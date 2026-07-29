import pymysql
import pymysql.cursors
from config import DB_CONFIG


def get_connection():
    """Buka koneksi baru ke database. Dipanggil per-request, ditutup
    setelah selesai (lihat pola pemakaian di auth.py / app.py)."""
    return pymysql.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        database=DB_CONFIG['database'],
        cursorclass=pymysql.cursors.DictCursor,  
        autocommit=False,
    )


def init_db():
    """Jalankan sekali di awal (atau lewat schema.sql manual) untuk
    membuat semua tabel kalau belum ada. Aman dipanggil berkali-kali
    karena pakai `CREATE TABLE IF NOT EXISTS`."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id            INT AUTO_INCREMENT PRIMARY KEY,
                    username      VARCHAR(50) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id            INT PRIMARY KEY,
                    total_wins         INT DEFAULT 0,
                    total_losses       INT DEFAULT 0,
                    fastest_win_turns  INT DEFAULT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS battles (
                    id           INT AUTO_INCREMENT PRIMARY KEY,
                    user_id      INT NOT NULL,
                    winner       VARCHAR(10) NOT NULL,
                    turns_taken  INT NOT NULL,
                    played_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS battle_logs (
                    id           INT AUTO_INCREMENT PRIMARY KEY,
                    battle_id    INT NOT NULL,
                    turn_number  INT NOT NULL,
                    message      VARCHAR(255) NOT NULL,
                    FOREIGN KEY (battle_id) REFERENCES battles(id) ON DELETE CASCADE
                )
            """)
        conn.commit()
    finally:
        conn.close()


def run_many(sql, param_list):
    """Bulk insert — dipakai untuk simpan semua battle_logs sekaligus
    dalam 1 koneksi (bukan 1 koneksi per baris) supaya efisien."""
    if not param_list:
        return
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.executemany(sql, param_list)
        conn.commit()
    finally:
        conn.close()


def run_query(sql, params=None, fetch=None):
    """Helper generik untuk query.
    fetch=None  -> untuk INSERT/UPDATE/DELETE, return lastrowid
    fetch='one' -> return 1 baris (dict) atau None
    fetch='all' -> return semua baris (list of dict)
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params or ())
            if fetch == 'one':
                result = cur.fetchone()
            elif fetch == 'all':
                result = cur.fetchall()
            else:
                result = cur.lastrowid
        conn.commit()
        return result
    finally:
        conn.close()
