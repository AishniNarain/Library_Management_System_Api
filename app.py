from flask import Flask, jsonify
from flask_restx import Api,Resource
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager,create_access_token,jwt_required
from flask_jwt_extended.exceptions import RevokedTokenError,NoAuthorizationError
from pymongo import MongoClient
from sqlalchemy import or_
from extensions import db,ma,mail
from models import TokenBlockList,User
import os

jwt = JWTManager()

import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__)

#initializing different parameters to the main application
app.config.from_pyfile('config.py')
db.init_app(app)
jwt.init_app(app)
ma.init_app(app)
migrate = Migrate(app, db)
mail.init_app(app)


# client = MongoClient("mongodb://localhost:27017/")
# client = MongoClient("mongodb://mongo-db:27017/")

# mongodb://172.29.0.2:27017/ for mongo-compass
client = MongoClient("mongodb://172.17.0.1:27018/")

api = Api(app,version='1.0', title='Library Management System Api',description='This is a sample API documentation for Library Management System. This documentation will provide all details related to the operations performed in a library.')
ns = api.namespace('api/v1', description="Version 1.0 of API")

#adding authorization header
api.authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

# load user
@jwt.user_lookup_loader
def user_lookup_callback(jwt_header, jwt_data):
    identity = jwt_data['sub']
    user = User.query.filter(or_(User.username == identity, User.email == identity)).one_or_none()
    return user

# error handlers
@jwt_required(refresh=True)
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    identity = jwt_data['sub']
    access_token = create_access_token(identity=identity,fresh=False)
    return jsonify({"message":"Token has expired","error":"expired_token","refreshed_access_token": access_token})

@app.errorhandler(RevokedTokenError)
def handle_revoked_token_error(error):
    return {'error': 'Token has been revoked'}, 401

@api.errorhandler(NoAuthorizationError)
def handle_no_authorization_error(error):
    return {'error': 'Missing Authorization Header'}, 401
    
@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header,jwt_data):
    jti = jwt_data['jti']
    token = db.session.query(TokenBlockList).filter(TokenBlockList.jti == jti).scalar()
    return token is not None

#for initializing routes
from books import route
from roles import route
from permissions import route
from users import route
from roles_and_permissions import route
from issue_books import route

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000,debug=True)
    # app.run(ssl_context=('cert.pem', 'key.pem'))