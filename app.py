from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.todo import Todo, TodoList
from resources.user import UserRegister, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-super-secret-key'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todo/<int:todo_id>')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(debug=True, port=5050)
