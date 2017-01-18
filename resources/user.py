from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from models.user import UserModel


parser = reqparse.RequestParser()
parser.add_argument('username', required=True, help='This field cannot be left blank')
parser.add_argument('password', required=True, help='This field cannot be left blank')


class UserRegister(Resource):
    def post(self):
        data = parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with this username already exists."}

        user = UserModel(**data)
        user.save_to_db()

        return user.json(), 201


class User(Resource):

    method_decorators = [jwt_required()]

    def get(self):
        user = UserModel.find_by_id(current_identity.id)

        return user.json()

    def delete(self):
        user = UserModel.find_by_id(current_identity.id)

        try:
            user.delete_from_db()
        except:
            return {"message": "An error occured deleting user"}, 500

        return {}, 204
