from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.todo import TodoModel


parser = reqparse.RequestParser()
parser.add_argument('task',
                    required=True,
                    help='Todo need a task')
parser.add_argument('completed',
                    type=bool,
                    required=True,
                    help='Todo need a status')


class Todo(Resource):

    method_decorators = [jwt_required()]

    def get(self, todo_id):
        todo = TodoModel.find_by_user_and_id(todo_id, current_identity.id)

        if todo:
            return todo.json(), 200

        return {"error": "No task found"}, 404

    def put(self, todo_id):
        data = parser.parse_args()
        data['user_id'] = current_identity.id

        todo = TodoModel.find_by_id(todo_id)

        if todo is None:
            todo = TodoModel(**data)
        else:
            todo.task = data['task']
            todo.completed = data['completed']

        todo.save_to_db()

        return todo.json()

    def delete(self, todo_id):
        todo = TodoModel.find_by_id(todo_id)

        if todo:
            todo.delete_from_db()
            return {}, 204

        return {"error": "No task found"}, 404


class TodoList(Resource):

    method_decorators = [jwt_required()]

    def get(self):
        todos = TodoModel.query.filter_by(user_id=current_identity.id)

        return {"todos": [todo.json() for todo in todos]}

    def post(self):
        data = parser.parse_args()
        data['user_id'] = current_identity.id

        todo = TodoModel(**data)

        try:
            todo.save_to_db()
        except:
            return {"message": "An error occured inserting the todo."}, 500

        return todo.json(), 201
