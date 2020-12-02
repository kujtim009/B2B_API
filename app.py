from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS, cross_origin
from blacklist import BLACKLIST
import urllib
import routes.mlfRoutes as mlfRoutes
import routes.userRoutes as userRoutes
import routes.cbdRoutes as cbdRoutes
import models.parameters as prm
from resources.user import TestAPI
from models.user import UserModel


app = Flask(__name__)
CORS(app)
## quoted = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=192.168.2.198\ITPLF;UID=" + prm.sql_username + ";PWD=" + prm.sql_password + ";DATABASE=InsertTool;Trusted_Connection=no;")
quotedDigitalOcean = urllib.parse.quote_plus("DRIVER={ODBC Driver 17 for SQL Server};SERVER=208.118.231.180,21201;UID=" +
                                             prm.sql_username + ";PWD=" + prm.sql_password + ";DATABASE=InsertTool;Trusted_Connection=no;")
quotedLocalPc = urllib.parse.quote_plus("DRIVER={SQL Server};SERVER=208.118.231.180,21201;UID=" +
                                        prm.sql_username + ";PWD=" + prm.sql_password + ";DATABASE=InsertTool;Trusted_Connection=no;")

app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(
    quotedDigitalOcean)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['JWT_SECRET_KEY'] = prm.jwt_secret_key_stored
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
app.config['ENV'] = ''

api = Api(app)

jwt = JWTManager(app)  # /auth


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    access_level = user.access_level
    return access_level


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'message': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required'
    }), 401


api.add_resource(TestAPI, '/test')
userRoutes.insertUserRoutes(api)
mlfRoutes.insertMlfRoutes(api)
cbdRoutes.insertCbdRoutes(api)


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
