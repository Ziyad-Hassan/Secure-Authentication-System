from flask import Blueprint, request, jsonify, current_app, send_file, make_response
from models import db, User
import bcrypt
import pyotp
import jwt
import datetime
import qrcode
import io

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('name') or not data.get('email_or_username') or not data.get('password'):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email_or_username=data.get('email_or_username')).first():
        return jsonify({'error': 'User already exists'}), 400

    # Hash password and generate 2FA secret
    hashed = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt())
    
    new_user = User(
        name=data.get('name'),
        email_or_username=data.get('email_or_username'),
        hashed_password=hashed.decode('utf-8'),
        role=data.get('role', 'User'),
        two_factor_secret=pyotp.random_base32()
    )
    db.session.add(new_user)
    db.session.commit()
    
    # Return success AND the QR code URL to display after registration
    return jsonify({
        'message': 'Registered successfully',
        'qr_url': f'/api/get-qr-code/{new_user.email_or_username}'
    }), 201

@auth_bp.route('/get-qr-code/<username>')
def get_qr_code(username):
    user = User.query.filter_by(email_or_username=username).first()
    if not user: return "User not found", 404
    
    uri = pyotp.totp.TOTP(user.two_factor_secret).provisioning_uri(name=user.email_or_username, issuer_name="SecureAuth")
    qr_img = qrcode.make(uri)
    buf = io.BytesIO()
    qr_img.save(buf, 'PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email_or_username=data.get('email_or_username')).first()

    # Step 1: Validate Password
    if not user or not bcrypt.checkpw(data.get('password').encode('utf-8'), user.hashed_password.encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Step 2: Request 2FA code (No QR code displayed here anymore)
    otp = data.get('totp_code')
    if not otp:
        return jsonify({
            'step': '2fa_required',
            'message': 'Password correct. Please enter your 6-digit code.'
        }), 200

    # Step 3: Verify 2FA and Issue Token
    if pyotp.TOTP(user.two_factor_secret).verify(otp):
        token = jwt.encode({
            'user_id': user.id, 'name': user.name, 'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        resp = make_response(jsonify({'token': token, 'name': user.name, 'role': user.role}))
        resp.set_cookie('token', token, httponly=True)
        return resp
    
    return jsonify({'error': 'Invalid 2FA code'}), 401