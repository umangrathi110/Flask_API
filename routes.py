from flask import Blueprint, request, jsonify
from models import db, User, Contact, Spam
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

api = Blueprint('api', __name__)
jwt = JWTManager()

@api.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'message': 'Phone number already registered'}), 400
    
    user = User(
        name=data['name'],
        phone=data['phone'],
        email=data.get('email'),
        password=data['password']
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(phone=data['phone']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.phone)
        return jsonify({'token': token}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/spam', methods=['POST'])
@jwt_required()
def mark_spam():
    data = request.json
    spam = Spam.query.filter_by(phone=data['phone']).first()
    if spam:
        spam.reports += 1
    else:
        spam = Spam(phone=data['phone'])
        db.session.add(spam)
    db.session.commit()
    return jsonify({'message': 'Number marked as spam'}), 200

@api.route('/search', methods=['GET'])
@jwt_required()
def search():
    query = request.args.get('query')
    search_by = request.args.get('search_by', 'name')
    results = []

    if search_by == 'name':
        results = User.query.filter(User.name.ilike(f'%{query}%')).all()
    elif search_by == 'phone':
        results = User.query.filter_by(phone=query).all()
    
    response = [{'name': user.name, 'phone': user.phone} for user in results]
    return jsonify(response), 200
