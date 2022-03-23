import flask
from flask import request, jsonify

from data import db_session
from data.users import User

blueprint = flask.Blueprint('user_api', __name__, template_folder='templates')


@blueprint.route('/api/users')
def get_jobs():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {'users': [item.to_dict(
            only=('id', 'name', 'about', 'email', 'hashed_password', 'created_date'))
            for item in users]})


@blueprint.route('/api/users/<int:user_id>', methods=['GET'])
def one_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    return jsonify({'users': user.to_dict(
        only=('id', 'name', 'about', 'email', 'hashed_password', 'created_date'))})


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    id_users = list([i.id for i in users])
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'about', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    for i in id_users:
        if int(i) == int(request.json['id']):
            return jsonify({'error': 'Id already exists'})
    user = User(
        id=request.json['id'],
        name=request.json['name'],
        about=request.json['about'],
        email=request.json['email'],
        hashed_password=request.json['hashed_password']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['DELETE'])
def delete_users(users_id):
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(users_id)
    if not users:
        return jsonify({'error': 'Not found'})
    db_sess.delete(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:users_id>', methods=['PUT'])
def edit_users(users_id):
    db_sess = db_session.create_session()
    id_users = db_sess.query(User).get(users_id)
    if not id_users:
        return jsonify({'error': 'Not found'})
    elif not all(key in request.json for key in
                 ['name', 'about', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    for user_ed in db_sess.query(User).filter(User.id == users_id):
        user_ed.name = request.json['name']
        user_ed.about = request.json['about']
        user_ed.email = request.json['email']
        user_ed.hashed_password = request.json['hashed_password']
    db_sess.commit()
    return jsonify({'success': 'OK'})
