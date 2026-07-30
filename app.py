from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, jsonify, request, session, redirect
from characters import Hero, Mage, Monster
from auth import auth_bp
from db import init_db, run_query, run_many
from config import SECRET_KEY
from datetime import datetime
from zoneinfo import ZoneInfo
import random
import functools



app = Flask(__name__)  
app.secret_key = SECRET_KEY
app.register_blueprint(auth_bp)

# Buat tabel users/user_stats kalau belum ada, sekali saat server start.
init_db()


def login_required(view_func):
    """Decorator: tolak akses ke route game kalau belum login.
    Dipakai dengan @login_required di atas route yang perlu proteksi."""
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return view_func(*args, **kwargs)
    return wrapper

def serialize_character(c, extra=None):
    """Ubah objek Character jadi dict biar bisa disimpan di session (cookie),
    yang cuma bisa nyimpan tipe data JSON-serializable, bukan objek Python."""
    data = {'hp': c.hp, 'alive': c.is_alive}
    if hasattr(c, 'mp'):
        data['mp'] = c.mp
    if extra:
        data.update(extra)
    return data


def restore_hero(data):
    """Bikin ulang objek Hero dari dict yang tersimpan di session, lalu
    timpa stat-nya (bukan bikin Hero baru dengan HP/MP penuh)."""
    h = Hero("Ziqi")
    h._hp = data['hp']
    h._mp = data['mp']
    h._is_alive = data['alive']
    h._is_blocking = data.get('is_blocking', False)
    return h


def restore_mage(data):
    m = Mage("Hazel")
    m._hp = data['hp']
    m._mp = data['mp']
    m._is_alive = data['alive']
    return m


def restore_monster(data):
    mo = Monster("Minotauruz")
    mo._hp = data['hp']
    mo._is_alive = data['alive']
    return mo


def load_battle():
    """Ambil objek hero/mage/monster dari session['battle']. Return None
    kalau belum ada battle aktif."""
    b = session.get('battle')
    if not b:
        return None
    return {
        'hero':        restore_hero(b['hero']),
        'mage':        restore_mage(b['mage']),
        'monster':     restore_monster(b['monster']),
        'battle_over': b['battle_over'],
        'log':         b['log'],
        'turn_count':  b['turn_count'],
    }


def save_battle_to_session(g: dict):
    """Simpan balik state battle (setelah dimutasi) ke session."""
    session['battle'] = {
        'hero':        serialize_character(g['hero'], {'is_blocking': g['hero']._is_blocking}),
        'mage':        serialize_character(g['mage']),
        'monster':     serialize_character(g['monster']),
        'battle_over': g['battle_over'],
        'log':         g['log'],
        'turn_count':  g['turn_count'],
    }
    session.modified = True


def build_state(g: dict, next_turn: str, messages: list, battle_over=False, winner=None):
    """Helper: kumpulkan semua state jadi 1 dict untuk dikirim ke browser."""
    h  = g['hero']
    m  = g['mage']
    mo = g['monster']
    return {
        'hero': {
            'hp': h.hp, 'max_hp': h.max_hp,
            'mp': h.mp, 'max_mp': h.max_mp,
            'alive': h.is_alive,
            'anim': h.get_animation_state()
        },
        'mage': {
            'hp': m.hp, 'max_hp': m.max_hp,
            'mp': m.mp, 'max_mp': m.max_mp,
            'alive': m.is_alive,
            'anim': m.get_animation_state()
        },
        'monster': {
            'hp': mo.hp, 'max_hp': mo.max_hp,
            'alive': mo.is_alive,
            'anim': mo.get_animation_state()
        },
        'messages':    messages,
        'next_turn':   next_turn,
        'battle_over': battle_over,
        'winner':      winner
    }


def save_battle_result(user_id: int, g: dict, winner: str):
    """Dipanggil SEKALI saat battle berakhir (menang atau kalah).
    Battle yang SEDANG berlangsung tidak pernah menyentuh database —
    semua log dikumpulkan di memori (`g['log']`) dulu, baru ditulis
    ke MySQL sekaligus di sini (1 batch insert, bukan 1 insert per
    aksi) supaya tidak lambat karena bolak-balik ke server jauh.
    """
    turns_taken = g['turn_count']
    played_at   = datetime.now(ZoneInfo("Asia/Jakarta"))

    battle_id = run_query(
        "INSERT INTO battles (user_id, winner, turns_taken, played_at) VALUES (%s, %s, %s, %s)",
        (user_id, winner, turns_taken, played_at)
    )

    log_rows = [(battle_id, i + 1, msg) for i, msg in enumerate(g['log'])]
    run_many(
        "INSERT INTO battle_logs (battle_id, turn_number, message) VALUES (%s, %s, %s)",
        log_rows
    )

    if winner == 'player':
        stats = run_query(
            "SELECT fastest_win_turns FROM user_stats WHERE user_id = %s",
            (user_id,), fetch='one'
        )
        current_fastest = stats['fastest_win_turns'] if stats else None
        if current_fastest is None or turns_taken < current_fastest:
            run_query(
                "UPDATE user_stats SET total_wins = total_wins + 1, fastest_win_turns = %s WHERE user_id = %s",
                (turns_taken, user_id)
            )
        else:
            run_query(
                "UPDATE user_stats SET total_wins = total_wins + 1 WHERE user_id = %s",
                (user_id,)
            )
    else:
        run_query(
            "UPDATE user_stats SET total_losses = total_losses + 1 WHERE user_id = %s",
            (user_id,)
        )


# ----------------------------------------------------------------
#  Halaman utama
# ----------------------------------------------------------------
@app.route('/')
@login_required
def index():
    return render_template('index.html', username=session.get('username'))


# ----------------------------------------------------------------
#  Mulai battle
# ----------------------------------------------------------------
@app.route('/start', methods=['POST'])
@login_required
def start():
    g = {
        'hero':        Hero("Ziqi"),
        'mage':        Mage("Hazel"),
        'monster':     Monster("Minotauruz"),
        'battle_over': False,
        'log':         [],
        'turn_count':  0,
    }
    save_battle_to_session(g)
    return jsonify(build_state(
        g,
        next_turn='hero',
        messages=['⚔ Battle dimulai! Giliran Ziqi.']
    ))


# ----------------------------------------------------------------
#  Proses aksi / attack
# ----------------------------------------------------------------
@app.route('/action', methods=['POST'])
@login_required
def action():
    g = load_battle()
    if not g or g.get('battle_over'):
        return jsonify({'error': 'Battle belum dimulai'}), 400

    data      = request.get_json()
    character = data.get('character')   
    act       = data.get('action')      

    h  = g['hero']
    m  = g['mage']
    mo = g['monster']
    messages = []
    g['turn_count'] += 1

    # === STEP 1: aksi player ===
    if character == 'hero' and h.is_alive:
        if act == 'block':
            messages.append(h.block())
        else:
            messages.append(h.attack(mo))

    elif character == 'mage' and m.is_alive:
        if act == 'skill':
            messages.append(m.cast_spell(mo))
        else:
            messages.append(m.attack(mo))

    # === STEP 2: cek status monster ===
    if not mo.is_alive:
        g['battle_over'] = True
        messages.append('🏆 Minotauruz dikalahkan! PARTY MENANG!')
        g['log'].extend(messages)
        save_battle_result(session['user_id'], g, winner='player')
        save_battle_to_session(g)
        return jsonify(build_state(g, 'none', messages, battle_over=True, winner='player'))

    # === STEP 3: turn monster ===
    should_monster_attack = (character == 'mage') or (character == 'hero' and not m.is_alive) or (character == 'mage' and not h.is_alive)

    if should_monster_attack:
        alive_targets = [c for c in (h, m) if c.is_alive]
        if alive_targets:
            target = random.choice(alive_targets)
            messages.append(mo.monster_turn(target))

        # === STEP 4: cek status player ===
        if not h.is_alive and not m.is_alive:
            g['battle_over'] = True
            messages.append('💀 Party kalah! Minotauruz menang.')
            g['log'].extend(messages)
            save_battle_result(session['user_id'], g, winner='monster')
            save_battle_to_session(g)
            return jsonify(build_state(g, 'none', messages, battle_over=True, winner='monster'))

    g['log'].extend(messages)

    # === STEP 5: next action ===
    if character == 'hero':
        next_turn = 'mage' if m.is_alive else 'hero'
    else:
        next_turn = 'hero' if h.is_alive else 'mage'

    save_battle_to_session(g)
    return jsonify(build_state(g, next_turn, messages))


# ----------------------------------------------------------------
#  Profil
# ----------------------------------------------------------------
@app.route('/profile')
@login_required
def profile():
    stats = run_query(
        "SELECT total_wins, total_losses, fastest_win_turns FROM user_stats WHERE user_id = %s",
        (session['user_id'],), fetch='one'
    )
    total = stats['total_wins'] + stats['total_losses']
    win_rate = round(stats['total_wins'] / total * 100, 1) if total > 0 else 0
    return render_template('profile.html', username=session.get('username'),
                            stats=stats, total=total, win_rate=win_rate)


# ----------------------------------------------------------------
#  Leaderboard
# ----------------------------------------------------------------
@app.route('/leaderboard')
@login_required
def leaderboard():
    rows = run_query("""
        SELECT u.username, s.total_wins, s.total_losses, s.fastest_win_turns
        FROM user_stats s
        JOIN users u ON u.id = s.user_id
        ORDER BY s.total_wins DESC, s.fastest_win_turns ASC
        LIMIT 20
    """, fetch='all')
    return render_template('leaderboard.html', username=session.get('username'), rows=rows)


# ----------------------------------------------------------------
#  Riwayat battle
# ----------------------------------------------------------------
@app.route('/history')
@login_required
def history():
    rows = run_query(
        "SELECT id, winner, turns_taken, played_at FROM battles WHERE user_id = %s ORDER BY played_at DESC LIMIT 30",
        (session['user_id'],), fetch='all'
    )
    return render_template('history.html', username=session.get('username'), rows=rows)


# ----------------------------------------------------------------
#  Detail 1 battle
# ----------------------------------------------------------------
@app.route('/history/<int:battle_id>')
@login_required
def history_detail(battle_id):
    battle = run_query(
        "SELECT id, winner, turns_taken, played_at FROM battles WHERE id = %s AND user_id = %s",
        (battle_id, session['user_id']), fetch='one'
    )
    if not battle:
        return "Battle tidak ditemukan", 404

    logs = run_query(
        "SELECT turn_number, message FROM battle_logs WHERE battle_id = %s ORDER BY turn_number ASC",
        (battle_id,), fetch='all'
    )
    return render_template('history_detail.html', username=session.get('username'),
                            battle=battle, logs=logs)


if __name__ == '__main__':
    app.run(debug=True)
