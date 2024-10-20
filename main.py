import datetime
from flask import *
from flasgger import Swagger
import sqlalchemy
from data import db_session
from flask import Flask, request, jsonify
from data.users import User
from data.groups import Group
from data.product_to_user import ProductToUser
from data.measurements import Measurements
from data.categories import Categories
from data.storage_conditions import StorageConditions
from data.products import Products

app = Flask(__name__)
swagger = Swagger(app)
db_session.global_init('db.db')


@app.route('/api/user', methods=['POST'])
def create_user():
    """
    Create a new user
    ---
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            login:
              type: string
              example: "vasya123"
            email:
              type: string
              example: "example@yandex.ru"
            password:
              type: string
              example: "123456"
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad request"
    """
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
        return jsonify({"status": "OK"})


@app.route('/api/login', methods=['GET'])
def login_user():
    """
        Retrieve user by login or email
        ---
        parameters:
          - name: user
            in: body
            required: true
            schema:
              type: object
              properties:
                login:
                  type: string
                  example: "john_doe"
                email:
                  type: string
                  example: "john.doe@example.com"
                password:
                  type: string
                  example: "supersecurepassword"
        responses:
          200:
            description: User details
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                login:
                  type: string
                  example: "john_doe"
                email:
                  type: string
                  example: "john.doe@example.com"
                group_id:
                  type: integer
                  example: 2
          400:
            description: Bad request
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Bad request"
          403:
            description: Forbidden
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Forbidden"
          404:
            description: User not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Not Found"
        """
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not request.json['password'] or not (request.json['login'] or request.json['email']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    try:
        db_sess = db_session.create_session()
        if request.json['login']:
            user = db_sess.query(User).filter(User.login == request.json['login'])
        else:
            user = db_sess.query(User).filter(User.email == request.json['email'])
        if not user:
            return make_response(jsonify({'error': 'Not Found'}), 404)
        if not user.check_password():
            return make_response(jsonify({'error': 'Forbidden'}), 403)
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        data = {'id': user.id, 'login': user.login}
        return jsonify(data)


@app.route('/api/register', methods=['POST'])
def register_user():
    """
    Create a new user
    ---
    parameters:
      - name: user
        in: body
        required: true
        schema:
          type: object
          properties:
            login:
              type: string
              example: "vasya123"
            email:
              type: string
              example: "example@yandex.ru"
            password:
              type: string
              example: "123456"
    responses:
      201:
        description: User created successfully
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Bad request"
    """
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
        return jsonify({"status": "OK"})


@app.route('/api/user/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """
        Get user details by ID
        ---
        parameters:
          - name: user_id
            in: path
            required: true
            type: integer
            description: The ID of the user to retrieve
        responses:
          200:
            description: User details
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                login:
                  type: string
                  example: "john_doe"
                email:
                  type: string
                  example: "john.doe@example.com"
                group_id:
                  type: integer
                  example: 2
          404:
            description: User not found
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Not found"
        """
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = {'id': user.id, 'login': user.login, 'email': user.email, 'group_id': user.group_id}
    return jsonify(data)


@app.route('/api/groups', methods=['POST'])
def create_group():
    """
       Create a new group
       ---
       parameters:
         - name: group
           in: body
           required: true
           schema:
             type: object
             properties:
               name:
                 type: string
                 example: "My Family"
       responses:
         201:
           description: Group created successfully
           schema:
             type: object
             properties:
               id:
                 type: integer
                 example: 1
         400:
           description: Bad request
           schema:
             type: object
             properties:
               error:
                 type: string
                 example: "Bad request"
       """
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif "name" not in request.json:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    try:
        db_sess = db_session.create_session()
        group = Group(
            name=request.json['name']
        )
        db_sess.add(group)
        db_sess.commit()
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        return jsonify({"status": "OK"})


@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
        Get a group by ID
        ---
        parameters:
          - name: group_id
            in: path
            required: true
            type: integer
            description: The ID of the group to retrieve
        responses:
          200:
            description: Group details
            schema:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "My Family"
          404:
            description: Group not found
        """
    db_sess = db_session.create_session()
    group = db_sess.query(Group).get(group_id)
    if not group:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = {'id': group.id, 'name': group.name}
    return jsonify(data)


@app.route('/api/products', methods=['POST'])
def upload_json():
    """
       Create a new item
       ---
       parameters:
         - name: item
           in: body
           required: true
           schema:
             type: object
             properties:
               name:
                 type: string
                 example: "Sample Item"
               userId:
                 type: integer
                 example: 1
               count:
                 type: integer
                 example: 10
               countUnits:
                 type: string
                 example: "pieces"
               storage_life:
                 type: string
                 example: "2 years"
               purchase_date:
                 type: string
                 example: "2024-01-01"
           description: Item to create
       responses:
         201:
           description: Item created
         400:
           description: Invalid input
       """
    form = request.get_json()
    if not form:
        return make_response(jsonify({'error': 'invalid error'}), 403)
    db_sess = db_session.create_session()
    product = Products(
        name=form["name"],
        freshness_duration=form['freshness_duration'],
        category_id=form['category_id'],
        image=form['image']
    )
    db_sess.add(product)
    db_sess.commit()
    return jsonify({'status': 'ok'})


@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """
    Get user details by ID
    ---
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: The ID of the user to retrieve
    responses:
      200:
        description: User details
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            login:
              type: string
              example: "john_doe"
            email:
              type: string
              example: "john.doe@example.com"
            group_id:
              type: integer
              example: 2
      404:
        description: User not found
    """
    db_sess = db_session.create_session()
    product = db_sess.query(Products).get(product_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = {"id": product.id, "name": product.name, "freshness_duration": product.freshness_duration,
            "category_id": product.category_id, "image": product.image}
    return jsonify(data)


@app.route('/api/products', methods=['GET'])
def get_products():
    db_sess = db_session.create_session()
    products = db_sess.query(Products)
    data = [{"id": i.id, "name": i.name, "freshness_duration": i.freshness_duration, "category_id": i.category_id,
             "image": i.image} for i in products]
    return jsonify(data)


@app.route('/api/products/<int:food_id>', methods=['DELETE'])
def delete_product(food_id):
    """
        Delete a product item by ID
        ---
        parameters:
          - name: food_id
            in: path
            type: integer
            required: true
            description: The ID of the product item to delete
        responses:
          200:
            description: ProductToUser item successfully deleted
          404:
            description: ProductToUser item not found
        """
    db_sess = db_session.create_session()
    product = db_sess.query(Products).get(food_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(product)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@app.route('/api/categories', methods=['POST'])
def create_categories():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
        for i in request.json:
            if "name" not in i:
                return make_response(jsonify({'error': 'Bad request'}), 400)
            category = Categories(
                name=request.json['name']
            )
            db_sess.add(category)
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        db_sess.commit()
        return jsonify({"status": "OK"})


@app.route('/api/categories', methods=['GET'])
def get_categories():
    db_sess = db_session.create_session()
    group = db_sess.query(Categories)
    data = [{"id": i.id, "name": i.name} for i in group]
    return jsonify(data)


@app.route('/api/measurements', methods=['POST'])
def create_measurements():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
        for i in request.json:
            if "name" not in i:
                return make_response(jsonify({'error': 'Bad request'}), 400)
            measurements = Measurements(
                name=request.json['name']
            )
            db_sess.add(measurements)
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        db_sess.commit()
        return jsonify({"status": "OK"})


@app.route('/api/measurements', methods=['GET'])
def get_measurements():
    db_sess = db_session.create_session()
    measurements = db_sess.query(Measurements)
    data = [{"id": i.id, "name": i.name} for i in measurements]
    return jsonify(data)


@app.route('/api/user-products', methods=['POST'])
def create_user_products():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
        for i in request.json:
            if all(key in i for key in
                   ['user_id', 'product_id', 'creation_date', 'measurement_id', 'count', 'storage_conditions_id']):
                return make_response(jsonify({'error': 'Bad request'}), 400)
            user_products = ProductToUser(
                user_id=request.json['user_id'],
                product_id=request.json['product_id'],
                creation_date=request.json['creation_date'],
                measurement_id=request.json['measurement_id'],
                count=request.json['count'],
                storage_conditions_id=request.json['storage_conditions_id']
            )
            db_sess.add(user_products)
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        db_sess.commit()
        return jsonify({"status": "OK"})


@app.route('/api/user-products', methods=['GET'])
def get_user_products():
    db_sess = db_session.create_session()
    user_products = db_sess.query(ProductToUser)
    data = [{"id": i.id, "user_id": i.user_id, "product_id": i.product_id, "creation_date": i.creation_date,
             "measurement_id": i.count, "count": i.measurement_id, "storage_conditions_id": i.storage_conditions_id}
            for i in user_products]
    return jsonify(data)


@app.route('/api/conditions', methods=['POST'])
def create_conditions():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
        for i in request.json:
            if 'name' not in i:
                return make_response(jsonify({'error': 'Empty request'}), 400)
            group = StorageConditions(name=i['name'])
            db_sess.add(group)
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        db_sess.commit()
        return jsonify({'status': 'ok'})


@app.route('/api/conditions/<int:conditions_id>', methods=['GET'])
def get_conditions(conditions_id):
    db_sess = db_session.create_session()
    con = db_sess.query(StorageConditions)
    if not con:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = [{'id': i.id, 'name': i.name} for i in con]
    return jsonify(data)



@app.route('/api/products', methods=['POST'])
def create_products():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    try:
        for i in request.json:
            if not all(key in request.json for key in ['name', 'freshness_duration', 'category_id', 'image']):
                db_sess = db_session.create_session()
                group = StorageConditions(name=request.json['name'],
                                          freshness_duration=request.json['freshness_duration'],
                                          category_id=request.json['category_id'],
                                          image=request.json['image']
                                          )
                db_sess.add(group)
                db_sess.commit()
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        return jsonify({"status": "OK"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
