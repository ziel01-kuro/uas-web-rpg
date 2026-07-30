from flask import Blueprint, request, jsonify, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from db import run_query
import pymysql

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@auth_bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    if len(username) < 3:
        return jsonify({'error': 'Username minimal 3 karakter'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password minimal 6 karakter'}), 400

    password_hash = generate_password_hash(password)

    try:
        user_id = run_query(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash)
        )
    except pymysql.err.IntegrityError:
        return jsonify({'error': 'Username sudah dipakai'}), 409

    run_query(
        "INSERT INTO user_stats (user_id, total_wins, total_losses) VALUES (%s, 0, 0)",
        (user_id,)
    )

    session['user_id']  = user_id
    session['username'] = username
    return jsonify({'ok': True, 'username': username})


@auth_bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = (data.get('username') or '').strip()
    password = data.get('password') or ''

    user = run_query(
        "SELECT id, username, password_hash FROM users WHERE username = %s",
        (username,), fetch='one'
    )

    if not user or not check_password_hash(user['password_hash'], password):
        return jsonify({'error': 'Username atau password salah'}), 401

    session['user_id']  = user['id']
    session['username'] = user['username']
    return jsonify({'ok': True, 'username': user['username']})


@auth_bp.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'ok': True})
