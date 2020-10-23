from resources.user import (
    UserRegister,
    User,
    UsersList,
    UserLogin,
    CheckAuth,
    TokenRefresh,
    UserLogout,
    Add_allowed_fields,
    TestAPI,
    removeUserFields,
    removeAllUserFields,
    AddUserTimePeriod,
    GetUserTimePeriod,
    AddUserCoins,
    GetUserCoins,
    GetUserPrmByName,
    AddUserPrm)
from models.user import UserModel
import models.parameters as prm
from resources.records import (GetAllFieldNames, getCurUserFields)


def insertUserRoutes(api):
    api.add_resource(UserRegister, '/register')
    api.add_resource(User, '/user/<int:user_id>')
    api.add_resource(UsersList, '/users')
    api.add_resource(UserLogin, '/auth')
    api.add_resource(CheckAuth, '/checkauth/<int:user_id>')
    api.add_resource(TokenRefresh, '/refresh')
    api.add_resource(UserLogout, '/logout')
    api.add_resource(getCurUserFields, '/usersField')
    api.add_resource(Add_allowed_fields, '/addUserFields')
    api.add_resource(removeUserFields, '/removeusrfields')
    api.add_resource(removeAllUserFields, '/removeallfields/<int:user_id>')
    api.add_resource(GetAllFieldNames, '/all_fields')
    api.add_resource(AddUserCoins, '/addUserCoins')
    api.add_resource(GetUserCoins, '/getcoins')
    api.add_resource(AddUserTimePeriod, '/addusertimeperiod')
    api.add_resource(GetUserTimePeriod, '/getusertimeperiod')
    api.add_resource(AddUserPrm, '/adduserprm')
    api.add_resource(GetUserPrmByName, '/getuserprm')
