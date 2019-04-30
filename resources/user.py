from flask_restful import Resource, reqparse, request
from passlib.hash import sha256_crypt
from models.user import UserModel, Userinfo, UserCoins
import models.parameters as prm
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    fresh_jwt_required,
    get_jwt_claims,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)
from blacklist import BLACKLIST


_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

_user_parser.add_argument('access_level',
                        type=str,
                        required=False,
                        help="This field cannot be blank."
                        )



_user_fields = reqparse.RequestParser()                     


class UserRegister(Resource):
    @fresh_jwt_required
    def post(self):
        if not UserModel.is_admin():
            return {'message': 'Admin privileges required'}
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400
        password = sha256_crypt.encrypt(data['password'])
        user = UserModel(data['username'], password, data['access_level'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201


class Add_allowed_fields(Resource):
    @fresh_jwt_required
    def post(self):
        # if not UserModel.is_admin():
        #     return {'message': 'Admin privileges required'}
        data = request.get_json()
        message = ""
        arg_usr_id = request.args.get('uid', None)

        for row in data:
            if arg_usr_id is None:
                userid = get_jwt_identity()
            else:
                userid = row["User_id"]

            fieldName = row["Field_name"]
            
            if Userinfo.fieldExist_in_user(userid, fieldName) is not True:
                userfields = Userinfo(userid, row["View_state"], row["File_name"], fieldName, row["Order"])
                userfields.save_to_db()
            else:
                message = ", one or more fields already existed on the list!"

        return {"message": "Fields added successfully{}".format(message)}, 201


class User(Resource):
    @fresh_jwt_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}
        return user.json()

    @fresh_jwt_required
    def delete(self, user_id):
        if not UserModel.is_admin():
            return {'message': 'Admin privileges required'}
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.delete_from_db()
        return {'message': 'User deleted'}, 200


class UsersList(Resource):
    @fresh_jwt_required
    def get(self):
        return {'Users': list(map(lambda x: x.json(), UserModel.query.all()))}


class UserLogin(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        # if user and safe_str_cmp(user.password, data['password']):
        if user and sha256_crypt.verify(data['password'], user.password):
            access_token = create_access_token(identity=user.ID, fresh=True)
            refresh_token = create_refresh_token(user.ID)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message': 'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200


class TestAPI(Resource):
    def get(self):
        return {'message': prm.sql_username}



class removeUserFields(Resource):
    @fresh_jwt_required
    def post(self):
        # if not UserModel.is_admin():
        #     return {'message': 'Admin privileges required'}
        data = request.get_json()
        message = ""
        for row in data["deletes"]:
            fieldID = row["id"]
            Userinfo.deletefield(fieldID)
        return {"message": "Rows deleted succesfuly"}, 201




class AddUserCoins(Resource):
    @fresh_jwt_required
    def get(self):
        cValue = 1000
        userid = get_jwt_identity()
        pckType = request.args.get('pck_type', None)
        if pckType:
            if pckType == "1":
                cValue = 1000
            elif pckType == "2":
                cValue = 10000
            elif pckType == "3":
                cValue = 1000000
        cost_per_coin  = 0.10 * cValue
        print("PCK TYPE: ".format(pckType))         
        userCoins = UserCoins(userid, cValue, cValue, cost_per_coin, 1)
        if userCoins.fieldExistInUserCoins(userid):
            userCoins.update(userid, cValue)
            # userCoins.query.filter_by(User_id=userid).first()
            # userCoins.C_purchased = cValue
            # userCoins.C_available = userCoins.C_available + cValue
            # userCoins.fieldExistInUserCoins = 0.10 * cValue
            # userCoins.db
        else:
            userCoins.save()
        return {'message': 'Thank You for your purchase!'}
    

class GetUserCoins(Resource):
    @fresh_jwt_required
    def get(self):
        userid = get_jwt_identity()
        usercoins = UserCoins.getUserCoins(userid)
        return {'coins': usercoins.C_available}