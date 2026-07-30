-- ================================================================
--  SAMPLE DATA (DUMMY DATA FOR TESTING & SCREENSHOTS)
--  Password for all sample accounts: password123
--  Werkzeug Hash: scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd
-- ================================================================

-- 1. Sample Users
INSERT INTO users (id, username, password_hash, created_at) VALUES
(1, 'admin_ziel', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-25 08:00:00'),
(2, 'shadow_knight', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-26 09:30:00'),
(3, 'dragon_slayer', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-27 14:15:00'),
(4, 'novice_player', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-28 16:45:00');

-- 2. Sample User Stats (Leaderboard & Profile)
INSERT INTO user_stats (user_id, total_wins, total_losses, fastest_win_turns) VALUES
(1, 15, 3, 4),
(2, 10, 5, 5),
(3, 7, 8, 6),
(4, 1, 4, 9);

-- 3. Sample Battle Records
INSERT INTO battles (id, user_id, winner, turns_taken, played_at) VALUES
(1, 1, 'player', 4, '2026-07-29 10:00:00'),
(2, 1, 'monster', 6, '2026-07-29 10:15:00'),
(3, 2, 'player', 5, '2026-07-29 11:30:00'),
(4, 3, 'player', 6, '2026-07-29 12:00:00'),
(5, 4, 'monster', 3, '2026-07-29 13:45:00');

-- 4. Sample Battle Logs (Log per giliran pertempuran)
INSERT INTO battle_logs (battle_id, turn_number, message) VALUES
-- Log Pertempuran 1 (Player Admin Win in 4 turns)
(1, 1, 'Prajurit menyerang Goblin dengan Tebasan Kritis sebesar 25 damage! HP Monster tersisa 75.'),
(1, 1, 'Goblin mencakar Prajurit sebesar 8 damage! HP Prajurit tersisa 92.'),
(1, 2, 'Prajurit menggunakan Ramuan Pemulihan (+20 HP)! HP Prajurit menjadi 100.'),
(1, 2, 'Goblin menyerang Prajurit sebesar 10 damage! HP Prajurit tersisa 90.'),
(1, 3, 'Prajurit melepaskan Skill Serangan Badai sebesar 45 damage! HP Monster tersisa 30.'),
(1, 3, 'Goblin menyerang Prajurit sebesar 7 damage! HP Prajurit tersisa 83.'),
(1, 4, 'Prajurit memberikan Pukulan Pamungkas sebesar 35 damage! Goblin telah dikalahkan!'),

-- Log Pertempuran 3 (Shadow Knight Win in 5 turns)
(3, 1, 'Penyihir menembakkan Bola Api sebesar 30 damage! HP Monster tersisa 70.'),
(3, 1, 'Raja Orc mengayunkan gada sebesar 12 damage! HP Penyihir tersisa 88.'),
(3, 2, 'Penyihir memasang Perisai Gaib untuk mengurangi damage.'),
(3, 2, 'Raja Orc menyerang Perisai Gaib, damage tertahan! HP Penyihir tersisa 85.'),
(3, 3, 'Penyihir melepaskan Petir Sambet sebesar 40 damage! HP Monster tersisa 30.'),
(3, 4, 'Raja Orc mengamuk dan menyerang sebesar 15 damage! HP Penyihir tersisa 70.'),
-- ================================================================
--  SAMPLE DATA (DUMMY DATA FOR TESTING & SCREENSHOTS)
--  Password for all sample accounts: password123
--  Werkzeug Hash: scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd
-- ================================================================

-- 1. Sample Users
INSERT INTO users (id, username, password_hash, created_at) VALUES
(1, 'admin_ziel', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-25 08:00:00'),
(2, 'shadow_knight', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-26 09:30:00'),
(3, 'dragon_slayer', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-27 14:15:00'),
(4, 'novice_player', 'scrypt:32768:8:1$G2mJQzIJ9t2qEgum$08d006c4956ad28cba12e0490254b249a97f08d24666a5bc7c517eb253be8624d5359924e77086237bd17234cdb0cb80dfe54c15d97d9dbc4c36f6eaaf4b1ccd', '2026-07-28 16:45:00');

-- 2. Sample User Stats (Leaderboard & Profile)
INSERT INTO user_stats (user_id, total_wins, total_losses, fastest_win_turns) VALUES
(1, 15, 3, 4),
(2, 10, 5, 5),
(3, 7, 8, 6),
(4, 1, 4, 9);

-- 3. Sample Battle Records
INSERT INTO battles (id, user_id, winner, turns_taken, played_at) VALUES
(1, 1, 'player', 4, '2026-07-29 10:00:00'),
(2, 1, 'monster', 6, '2026-07-29 10:15:00'),
(3, 2, 'player', 5, '2026-07-29 11:30:00'),
(4, 3, 'player', 6, '2026-07-29 12:00:00'),
(5, 4, 'monster', 3, '2026-07-29 13:45:00');

-- 4. Sample Battle Logs (Log per giliran pertempuran)
INSERT INTO battle_logs (battle_id, turn_number, message) VALUES
-- Log Pertempuran 1 (Player Admin Win in 4 turns)
(1, 1, 'Prajurit menyerang Goblin dengan Tebasan Kritis sebesar 25 damage! HP Monster tersisa 75.'),
(1, 1, 'Goblin mencakar Prajurit sebesar 8 damage! HP Prajurit tersisa 92.'),
(1, 2, 'Prajurit menggunakan Ramuan Pemulihan (+20 HP)! HP Prajurit menjadi 100.'),
(1, 2, 'Goblin menyerang Prajurit sebesar 10 damage! HP Prajurit tersisa 90.'),
(1, 3, 'Prajurit melepaskan Skill Serangan Badai sebesar 45 damage! HP Monster tersisa 30.'),
(1, 3, 'Goblin menyerang Prajurit sebesar 7 damage! HP Prajurit tersisa 83.'),
(1, 4, 'Prajurit memberikan Pukulan Pamungkas sebesar 35 damage! Goblin telah dikalahkan!'),

-- Log Pertempuran 3 (Shadow Knight Win in 5 turns)
(3, 1, 'Penyihir menembakkan Bola Api sebesar 30 damage! HP Monster tersisa 70.'),
(3, 1, 'Raja Orc mengayunkan gada sebesar 12 damage! HP Penyihir tersisa 88.'),
(3, 2, 'Penyihir memasang Perisai Gaib untuk mengurangi damage.'),
(3, 2, 'Raja Orc menyerang Perisai Gaib, damage tertahan! HP Penyihir tersisa 85.'),
(3, 3, 'Penyihir melepaskan Petir Sambet sebesar 40 damage! HP Monster tersisa 30.'),
(3, 4, 'Raja Orc mengamuk dan menyerang sebesar 15 damage! HP Penyihir tersisa 70.'),
(3, 5, 'Penyihir menggunakan Ledakan Sihir sebesar 35 damage! Raja Orc berhasil ditumbangkan!');