from datetime import timedelta
from flask_restful import Resource, reqparse, request
from passlib.hash import sha256_crypt
from models.user import UserModel, UserTimePeriod, Userinfo, UserCoins, UserPrm
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
import json
from blacklist import BLACKLIST
from models.loging import Loging


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
            fileName = row["File_name"]
            if Userinfo.fieldExist_in_user(userid, fieldName, fileName) is not True:
                userfields = Userinfo(
                    userid, row["View_state"], fileName, fieldName, row["Order"])
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
        print(
            "LOGINNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        # if user and safe_str_cmp(user.password, data['password']):
        if user and sha256_crypt.verify(data['password'], user.password):

            if int(user.access_level) >= 2 and UserTimePeriod.timePeriodExists(user.ID):
                if UserTimePeriod.getTimePeriod(user.ID) <= 0:
                    return {'message': 'Your subscription has expired, contact us for more details!'}, 401
            expires = timedelta(minutes=60)
            access_token = create_access_token(
                identity=user.ID, fresh=True, expires_delta=expires)
            refresh_token = create_refresh_token(user.ID)
            logPrmData = data.copy()
            logPrmData.pop('password')
            log = Loging(
                None, user.ID, data['username'], "Login success", json.dumps(logPrmData), None, str(request.remote_addr))
            log.save()
            return {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'userId': user.ID,
                'accessLevel': user.access_level,
                'expiresIn': UserTimePeriod.getTimePeriod(user.ID)
            }, 200
        log = Loging(
            None, user.ID, data['username'], "Login Failed", json.dumps(logPrmData), None, str(request.remote_addr))
        log.save()
        return {'message': 'Invalid credentials'}, 401


class CheckAuth(Resource):
    @fresh_jwt_required
    def get(self, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User not found'}, 401
        else:
            if int(user.access_level) >= 2 and UserTimePeriod.timePeriodExists(user.ID):
                if UserTimePeriod.getTimePeriod(user.ID) <= 0:
                    return {'message': 'Your subscription has expired, contact us for more details!'}, 401
        return {
            'userId': user.ID,
            'accessLevel': user.access_level,
            'expiresIn': UserTimePeriod.getTimePeriod(user.ID)
        }, 200

    # def get(cls):
    #     data = _user_parser.parse_args()
    #     user = UserModel.find_by_username(data['username'])
    #     # if user and safe_str_cmp(user.password, data['password']):
    #     if user and sha256_crypt.verify(data['password'], user.password):
    #         access_token = create_access_token(identity=user.ID, fresh=True)
    #         refresh_token = create_refresh_token(user.ID)
    #         return {
    #             'access_token': access_token,
    #             'refresh_token': refresh_token,
    #             'userId': user.ID,
    #             'accessLevel': user.access_level
    #         }, 200
    #     return {'message': 'Invalid credentials'}, 401


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


class removeAllUserFields(Resource):
    @fresh_jwt_required
    def post(self, user_id):
        Userinfo.deleteAllField(user_id)
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
        cost_per_coin = 0.10 * cValue
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


class GetUserTimePeriod(Resource):
    @fresh_jwt_required
    def get(self):
        userId = get_jwt_identity()
        prmUserID = request.args.get('uid', None)
        mainUserID = prmUserID if prmUserID else userId
        userTime = UserTimePeriod.getTimePeriodFull(mainUserID)
        if userTime is not None:
            return {
                'CreatedDate': userTime['CreatedDate'],
                'ExpirationDate': userTime['ExpirationDate'],
                'Dayes': userTime['Dayes']
            }
        return {'message': "Time period is not asigned to this user!"}, 404


class GetUserPrmByName(Resource):
    @fresh_jwt_required
    def get(self, prmName=None):
        userId = get_jwt_identity()
        jsonParameter = None
        if prmName is None:
            reqPrmName = request.args.get('prmname', None)
            prmUserID = request.args.get('uid', None)
            if reqPrmName is None:
                return {'message': "You need to specify a parameter name!"}
            else:
                if prmUserID is not None:
                    userParameter = UserPrm.getUserParameter(
                        prmUserID, reqPrmName)
                else:
                    userParameter = UserPrm.getUserParameter(
                        userId, reqPrmName)
                if userParameter is not None:
                    try:
                        jsonParameter = eval(str(userParameter.prm_value))
                    except:
                        jsonParameter = None

        else:
            if userParameter is not None:
                if prmUserID is not None:
                    userParameter = UserPrm.getUserParameter(
                        prmUserID, prmName)
                else:
                    userParameter = UserPrm.getUserParameter(userId, prmName)
                jsonParameter = eval(str(userParameter.prm_value))
        return {'prm_value': jsonParameter}


class AddUserPrm(Resource):
    @fresh_jwt_required
    def post(self):
        userId = get_jwt_identity()
        prmUserID = request.args.get('uid', None)
        mainUserID = prmUserID if prmUserID else userId

        data = request.get_json()
        print("JSON:", data)

        print("prm_name:", data["prm_name"])
        print("prm_value:", data["prm_value"])
        print("prm_value:", data["prm_description"])

        userParameter = UserPrm(
            int(mainUserID), data["prm_name"], json.dumps(data["prm_value"]), data["prm_description"])
        if userParameter.prmExist(mainUserID, data["prm_name"]):
            userParameter.update(
                mainUserID, data["prm_name"], data["prm_value"])
            return {'message': 'Parameter Updated succesfuly!'}
        else:
            userParameter.save()
            return {'message': 'Parameter Added succesfuly!'}


class AddUserTimePeriod(Resource):
    @fresh_jwt_required
    def post(self):
        userId = get_jwt_identity()
        prmUserID = request.args.get('uid', None)
        mainUserID = prmUserID if prmUserID else userId

        data = request.get_json()
        print("JSON:", data)

        userTimePeriod = UserTimePeriod(
            int(mainUserID), data["CreateDate"], data["ExpirationDate"])
        if userTimePeriod.timePeriodExists(mainUserID):
            userTimePeriod.update()
            return {'message': 'User Time Period Updated succesfuly!'}
        else:
            userTimePeriod.save()
            return {'message': 'User Time Period Added succesfuly!'}
