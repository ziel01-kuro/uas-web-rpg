// ================================================================
//  CONFIG SPRITE SHEET
// ================================================================
const SHEETS = {
    hero: {
        idle: ['hero_idle.png', 4, 6, 128],
        attack: ['hero_attack.png', 5, 10, 128],
        block: ['hero_block.png', 5, 8, 128],
        dead: ['hero_dead.png', 6, 8, 128],
    },
    mage: {
        idle: ['mage_idle.png', 7, 8, 128],
        attack: ['mage_attack.png', 14, 16, 128],
        meteor: ['mage_attack.png', 14, 16, 128],
        dead: ['mage_dead.png', 6, 8, 128],
    },
    monster: {
        idle: ['monster_idle.png', 10, 8, 128],
        attack: ['monster_attack.png', 5, 10, 128],
        dead: ['monster_dead.png', 5, 8, 128],
    },
};
const MAX = { hero: { hp: 120, mp: 20 }, mage: { hp: 80, mp: 90 }, monster: { hp: 375 } };

let currentTurn = null;
let busy = false;
let animTimers = {};
let deadState = { hero: false, mage: false, monster: false };

// ================================================================
//  ENGINE ANIMASI SPRITE SHEET
// ================================================================
function playSheet(character, action, loop = true) {
    const el = document.getElementById('inner-' + character);
    const [file, totalFrames, fps, frameW, playFrames] = SHEETS[character][action];
    const frames = playFrames || totalFrames;

    el.style.backgroundImage = `url('/static/sprites/${file}')`;
    el.style.backgroundSize = `${totalFrames * frameW}px 128px`;

    if (animTimers[character]) clearInterval(animTimers[character]);

    let frame = 0;
    el.style.backgroundPosition = '0px 0px';

    animTimers[character] = setInterval(() => {
        frame++;
        if (frame >= frames) {
            if (loop) {
                frame = 0;
            } else {
                clearInterval(animTimers[character]);
                frame = frames - 1;
                el.style.backgroundPosition = `-${frame * frameW}px 0px`;
                return;
            }
        }
        el.style.backgroundPosition = `-${frame * frameW}px 0px`;
    }, 1000 / fps);
}

function idle(character) { playSheet(character, 'idle', true); }

function playActionThenIdle(character, action, totalMs) {
    return new Promise(resolve => {
        playSheet(character, action, false);
        setTimeout(() => { idle(character); resolve(); }, totalMs);
    });
}

function playDeath(character) { playSheet(character, 'dead', false); }

// ================================================================
//  UTIL
// ================================================================
const sleep = ms => new Promise(r => setTimeout(r, ms));

function addLog(msg, type = '') {
    const log = document.getElementById('battle-log');
    const entry = document.createElement('div');
    entry.className = 'log-entry ' + type;
    entry.textContent = msg;
    log.prepend(entry);
}

function updateBar(id, val, maxVal, suffix) {
    const bar = document.getElementById('bar-' + id);
    const num = document.getElementById('val-' + id);
    const pct = Math.max(0, (val / maxVal) * 100);
    bar.style.width = pct + '%';
    if (id.includes('hp')) {
        bar.className = 'bar-fill hp-fill';
        if (pct <= 30) bar.classList.add('low');
        else if (pct <= 60) bar.classList.add('mid');
    }
    if (num) num.textContent = `${val}/${maxVal} ${suffix}`;
}

function setGlow(character) {
    ['hero', 'mage', 'monster'].forEach(c => document.getElementById('glow-' + c).classList.remove('show'));
    if (character) document.getElementById('glow-' + character).classList.add('show');
}

function lockButtons() { document.querySelectorAll('.btn').forEach(b => b.disabled = true); }
function unlockButtons() { document.querySelectorAll('.btn').forEach(b => b.disabled = false); }

// ================================================================
//  TURNS
// ================================================================
function setTurn(turn, heroAlive, mageAlive) {
    if (turn === 'hero' && !heroAlive && mageAlive) turn = 'mage';
    if (turn === 'mage' && !mageAlive && heroAlive) turn = 'hero';
    currentTurn = turn;

    const label = document.getElementById('turn-label');
    const btns = document.getElementById('skill-buttons');

    if (turn === 'hero') {
        label.innerHTML = 'Giliran <span>ZIQI</span>';
        btns.innerHTML = `
  <button class="btn btn-attack" onclick="doAction('hero','attack')">Serang</button>
  <button class="btn btn-block"  onclick="doAction('hero','block')">Block</button>`;
    } else if (turn === 'mage') {
        label.innerHTML = 'Giliran <span>HAZEL</span>';
        btns.innerHTML = `
  <button class="btn btn-attack" onclick="doAction('mage','attack')">Serang</button>
  <button class="btn btn-skill"  onclick="doAction('mage','skill')">Meteor</button>`;
    }
    setGlow(turn);
}

// ================================================================
//  START BATTLE
// ================================================================
async function startBattle() {
    const res = await fetch('/start', { method: 'POST' });
    const data = await res.json();

    document.getElementById('battle-log').innerHTML = '';
    deadState = { hero: false, mage: false, monster: false };

    updateBar('hero-hp', data.hero.hp, MAX.hero.hp, 'HP');
    updateBar('hero-mp', data.hero.mp, MAX.hero.mp, 'MP');
    updateBar('mage-hp', data.mage.hp, MAX.mage.hp, 'HP');
    updateBar('mage-mp', data.mage.mp, MAX.mage.mp, 'MP');
    updateBar('monster-hp', data.monster.hp, MAX.monster.hp, 'HP');

    idle('hero'); idle('mage'); idle('monster');

    data.messages.forEach(m => addLog(m));
    setTurn(data.next_turn, true, true);
    unlockButtons();
}

// ================================================================
//  ACTION
// ================================================================
async function doAction(character, action) {
    if (busy) return;
    busy = true;
    lockButtons();

    try {
        if (character === 'hero' && action === 'block') {
            await playActionThenIdle('hero', 'block', 550);
        } else {
            await playActionThenIdle(character, 'attack', 550);
        }

        const res = await fetch('/action', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ character, action })
        });
        const data = await res.json();

        updateBar('hero-hp', data.hero.hp, MAX.hero.hp, 'HP');
        updateBar('hero-mp', data.hero.mp, MAX.hero.mp, 'MP');
        updateBar('mage-hp', data.mage.hp, MAX.mage.hp, 'HP');
        updateBar('mage-mp', data.mage.mp, MAX.mage.mp, 'MP');
        updateBar('monster-hp', data.monster.hp, MAX.monster.hp, 'HP');

        for (const msg of data.messages) {
            addLog(msg, data.battle_over && data.winner ? (data.winner === 'player' ? 'win' : 'lose') : '');
            await sleep(120);
        }

        const monsterMsg = data.messages.find(m => m.includes('👾'));
        if (monsterMsg && data.monster.alive) {
            await sleep(150);
            await playActionThenIdle('monster', 'attack', 550);
        }

        await sleep(100);
        let justDied = false;
        if (!data.hero.alive && !deadState.hero) {
            deadState.hero = true;
            playDeath('hero');
            justDied = true;
        }
        if (!data.mage.alive && !deadState.mage) {
            deadState.mage = true;
            playDeath('mage');
            justDied = true;
        }
        if (!data.monster.alive && !deadState.monster) {
            deadState.monster = true;
            playDeath('monster');
            justDied = true;
        }
        if (justDied) await sleep(700);

        if (data.battle_over) {
            await sleep(300);
            showResult(data.winner);
        } else {
            setTurn(data.next_turn, data.hero.alive, data.mage.alive);
            unlockButtons();
        }

    } catch (err) {
        addLog('Error: ' + err.message);
        unlockButtons();
    }

    busy = false;
}

// ================================================================
//  RESULT SCREEN
// ================================================================
function showResult(winner) {
    const screen = document.getElementById('result-screen');
    const box = document.getElementById('result-box');
    const title = document.getElementById('result-title');
    const desc = document.getElementById('result-desc');

    if (winner === 'player') {
        box.className = 'result-box win';
        title.textContent = 'VICTORY!';
        desc.textContent = 'Party berhasil mengalahkan Minotauruz!';
    } else {
        box.className = 'result-box lose';
        title.textContent = 'DEFEAT';
        desc.textContent = 'Minotauruz terlalu kuat. Coba lagi!';
    }
    screen.classList.add('show');
    setGlow(null);
    unlockButtons();
}

function resetResult() {
    document.getElementById('result-screen').classList.remove('show');
    startBattle();
}

async function doLogout() {
    await fetch('/api/logout', { method: 'POST' });
    window.location.href = '/login';
}

document.addEventListener('DOMContentLoaded', () => {
    idle('hero');
    idle('mage');
    idle('monster');
});
