from sqlalchemy.sql.functions import count
from unicodedata import category
import datetime
from data.users import User
from data.foods import Food
from flask import *
from flasgger import Swagger
from data import db_session
from flask import Flask, request, jsonify

app = Flask(__name__)
swagger = Swagger(app)
db_session.global_init('db/db.db')


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


@app.route('/api/foods', methods=['POST'])
def upload_json():
    if request.method == 'POST':
        form = request.get_json()
        print(form)
        if not form:
            return make_response(jsonify({'error': 'invalid error'}), 403)
        db_sess = db_session.create_session()
        d, m, y = map(int, form['purchase_date'].split('-'))
        food = Food(
            name=form["name"],
            storage_life=form['storage_life'],
            category=form['category'],
            count=form['count'],
            count_units=form['count_units'],
            purchase_date=datetime.date(d, m, y),
            user_id=form['user_id']
        )
        db_sess.add(food)
        db_sess.commit()
        return make_response(jsonify({'status': 'ok'}), 200)
    else:
        return make_response(jsonify({'status': 'error'}), 400)


@app.route('/api/foods/<int:food_id>', methods=['GET'])
def get_user(food_id):
    db_sess = db_session.create_session()
    food = db_sess.query(Food).get(food_id)
    if not food:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = {'id': food.id, 'login': food.login, 'email': food.email, 'group_id': food.group_id}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
