from flask import *
from flasgger import Swagger
import sqlalchemy
from data import db_session
from data.users import User
from data.groups import Group

app = Flask(__name__)
swagger = Swagger(app)
db_session.global_init('db.db')


@app.route('/api/vasya', methods=['GET'])
def vazya():
    """
        Greeting endpoint.
        ---
        responses:
          200:
            description: A greeting message
            schema:
              type: object
              properties:
                message:
                  type: string
        """
    return {"message": "Hello, World!"}


@app.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['login', 'email', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    try:
        db_sess = db_session.create_session()
        users = User(
            login=request.json['login'],
            email=request.json['email']
        )
        users.set_password(request.json['password'])
        db_sess.add(users)
        db_sess.commit()
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        return jsonify({'id': users.id})


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = {'id': user.id, 'login': user.login, 'email': user.email, 'group_id': user.group_id}
    return jsonify(data)


@app.route('/api/groups', methods=['POST'])
def create_group():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['login', 'email', 'password']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    try:
        db_sess = db_session.create_session()
        group = Group(
            login=request.json['name']
        )
        db_sess.add(group)
        db_sess.commit()
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        return jsonify({'id': group.id})


@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    db_sess = db_session.create_session()
    group = db_sess.query(Group).get(group_id)
    if not group:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = {'id': group.id, 'name': group.name}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
