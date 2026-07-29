-- ================================================================
--  schema.sql — Struktur tabel database
--
--  File ini untuk REFERENSI dan dokumentasi (screenshot untuk laporan
--  UAS poin 5). Tabel sebenarnya dibuat otomatis oleh db.py:init_db()
--  saat app.py pertama kali jalan — kamu tidak perlu run file ini
--  manual kecuali mau lihat/edit struktur lewat phpMyAdmin filess.io.
--
--  Cakupan: login (users), leaderboard & profil (user_stats),
--  riwayat battle (battles, battle_logs). Tabel monster CRUD SENGAJA
--  tidak dibuat — di luar scope untuk saat ini.
-- ================================================================

CREATE TABLE IF NOT EXISTS users (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    username      VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_stats (
    user_id            INT PRIMARY KEY,
    total_wins         INT DEFAULT 0,
    total_losses       INT DEFAULT 0,
    fastest_win_turns  INT DEFAULT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS battles (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    winner       VARCHAR(10) NOT NULL,   -- 'player' atau 'monster'
    turns_taken  INT NOT NULL,
    played_at    DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS battle_logs (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    battle_id    INT NOT NULL,
    turn_number  INT NOT NULL,
    message      VARCHAR(255) NOT NULL,
    FOREIGN KEY (battle_id) REFERENCES battles(id) ON DELETE CASCADE
);



