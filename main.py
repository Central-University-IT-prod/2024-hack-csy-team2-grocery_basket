import datetime
from flask import *
from flasgger import Swagger
import sqlalchemy
from data import db_session
from flask import Flask, request, jsonify

from data.Products import Products
from data.users import User
from data.groups import Group
from data.product_to_user import ProductToUser
from data.measurements import Measurements
from data.categories import Categories
from data.storage_conditions import StorageConditions

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
    return jsonify({'status': 'ok'})


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
                  example: "{{sensitive data}}"
                password:
                  type: string
                  example: "{{sensitive data}}"
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
                  example: "{{sensitive data}}"
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
              example: "{{sensitive data}}"
            password:
              type: string
              example: "{{sensitive data}}"
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
    return jsonify({'status': 'ok'})


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
                  example: "{{sensitive data}}"
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
    elif not all(key in request.json for key in
                 ['login', 'email', 'password']):
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
    return jsonify({'status': 'ok'})


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


@app.route('/api/foods', methods=['POST'])
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
    if request.method == 'POST':
        form = request.get_json()
        print(form)
        if not form:
            return make_response(jsonify({'error': 'invalid error'}), 403)
        db_sess = db_session.create_session()
        d, m, y = map(int, form['purchase_date'].split('-'))
        product = ProductToUser(
            name=form["name"],
            storage_life=form['storage_life'],
            category=form['category'],
            count=form['count'],
            count_units=form['count_units'],
            purchase_date=datetime.date(d, m, y),
            user_id=form['user_id']
        )
        db_sess.add(product)
        db_sess.commit()
        return make_response(jsonify({'status': 'ok'}), 200)
    else:
        return make_response(jsonify({'status': 'error'}), 400)
    return jsonify({'status': 'ok'}, 200)


@app.route('/api/foods/<int:food_id>', methods=['GET'])
def get_food(food_id):
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
    product = db_sess.query(ProductToUser).get(food_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = {'id': product.id, 'login': product.login, 'email': product.email, 'group_id': product.group_id}
    return jsonify(data)


@app.route('/api/foods/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
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
    product = db_sess.query(ProductToUser).get(food_id)
    if not product:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(product)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@app.route('/api/categories', methods=['POST'])
def create_categories():
    """
       Создание новых категорий
       ---
       parameters:
         - name: category
           in: body
           required: true
           schema:
             type: array
             items:
               type: object
               properties:
                 name:
                   type: string
                   example: "Категория 1"
       responses:
         200:
           description: Категории успешно созданы
           schema:
             type: object
             properties:
               status:
                 type: string
                 example: "ok"
         400:
           description: Ошибка в запросе
           schema:
             type: object
             properties:
               error:
                 type: string
                 example: "Bad request"
       """
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
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
        return jsonify({'status: ok'})


@app.route('/api/categories', methods=['GET'])
def get_categories():
    """
       Получение всех категорий
       ---
       responses:
         200:
           description: Список категорий
           schema:
             type: array
             items:
               type: object
               properties:
                 id:
                   type: integer
                   example: 1
                 name:
                   type: string
                   example: "Категория 1"
         404:
           description: Категории не найдены
           schema:
             type: object
             properties:
               error:
                 type: string
                 example: "Not found"
       """
    db_sess = db_session.create_session()
    group = db_sess.query(Categories)
    data = [{"id": i.id, "name": i.name} for i in group]
    return jsonify(data)


@app.route('/api/measurements', methods=['POST'])
def create_measurements():
    """
        Создание новых измерений
        ---
        parameters:
          - name: measurement
            in: body
            required: true
            schema:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: "Измерение 1"
        responses:
          200:
            description: Измерения успешно созданы
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "ok"
          400:
            description: Ошибка в запросе
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Bad request"
        """
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
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
        return jsonify({'status': 'ok'})


@app.route('/api/measurements', methods=['GET'])
def get_measurements():
    """
        Получение всех измерений
        ---
        responses:
          200:
            description: Список измерений
            schema:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Измерение 1"
          404:
            description: Измерения не найдены
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Not found"
        """
    db_sess = db_session.create_session()
    measurements = db_sess.query(Measurements)
    data = [{"id": i.id, "name": i.name} for i in measurements]
    return jsonify(data)


@app.route('/api/user-products', methods=['POST'])
def create_user_products():
    """
        Создание пользовательских продуктов
        ---
        parameters:
          - name: user_product
            in: body
            required: true
            schema:
              type: array
              items:
                type: object
                properties:
                  user_id:
                    type: integer
                    example: 1
                  product_id:
                    type: integer
                    example: 1
                  creation_date:
                    type: string
                    format: date
                    example: "2023-10-01"
                  measurement_id:
                    type: integer
                    example: 1
                  count:
                    type: integer
                    example: 10
                  storage_conditions_id:
                    type: integer
                    example: 1
        responses:
          200:
            description: Пользовательские продукты успешно созданы
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "ok"
          400:
            description: Ошибка в запросе
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Bad request"
        """
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
        return make_response(jsonify({'error': 'Bad request'}), 400)
    return jsonify({'status': 'ok'})


@app.route('/api/user-products', methods=['GET'])
def get_user_products():
    """
      Получение всех пользовательских продуктов
      ---
      responses:
        200:
          description: Список пользовательских продуктов
          schema:
            type: array
            items:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "Продукт 1"
        404:
          description: Продукты не найдены
          schema:
            type: object
            properties:
              error:
                type: string
                example: "Not found"
    """
    db_sess = db_session.create_session()
    user_products = db_sess.query(Measurements)
    data = [{"id": i.id, "name": i.name} for i in user_products]
    return jsonify(data)


@app.route('/api/conditions', methods=['POST'])
def create_conditions():
    """
        Создание новых условий хранения
        ---
        parameters:
          - name: condition
            in: body
            required: true
            schema:
              type: array
              items:
                type: object
                properties:
                  name:
                    type: string
                    example: "Условие 1"
        responses:
          200:
            description: Условия хранения успешно созданы
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "ok"
          400:
            description: Ошибка в запросе
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Empty request"
        """
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    db_sess = db_session.create_session()
    try:
        group = StorageConditions(name=request.json['name'])
        db_sess.add(group)
    except sqlalchemy.exc.StatementError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Bad request'}), 400)
    else:
        db_sess.commit()
        return jsonify({'status': 'ok'})


@app.route('/api/conditions/', methods=['GET'])
def get_conditions():
    """
       Получение всех условий хранения
       ---
       responses:
         200:
           description: Список условий хранения
           schema:
             type: array
             items:
               type: object
               properties:
                 id:
                   type: integer
                   example: 1
                 name:
                   type: string
                   example: "Условие 1"
         404:
           description: Условия хранения не найдены
           schema:
             type: object
             properties:
               error:
                 type: string
                 example: "Not found"
       """
    db_sess = db_session.create_session()
    con = db_sess.query(StorageConditions)
    if not con:
        return make_response(jsonify({'error': 'Not found'}), 404)
    data = [{'id': i.id, 'name': i.name} for i in con]
    return jsonify(data)


@app.route('/api/products', methods=['POST'])
def create_products():
    """
        Создание нового продукта
        ---
        parameters:
          - name: product
            in: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Продукт 1"
                freshness_duration:
                  type: integer
                  example: 7
                category_id:
                  type: integer
                  example: 1
                image:
                  type: string
                  example: "http://example.com/image.png"
        responses:
          200:
            description: Продукт успешно создан
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: "ok"
          400:
            description: Ошибка в запросе
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: "Empty request"
        """
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    try:
        if not all(key in request.json for key in ['name', 'freshness_duration', 'category_id', 'image']):
            return make_response(jsonify({'error': 'Empty request'}), 400)
        db_sess = db_session.create_session()
        group = Products(name=request.json['name'],
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
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
