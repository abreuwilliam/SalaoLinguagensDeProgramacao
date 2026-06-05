from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Api
from dotenv import load_dotenv
from flasgger import Swagger
from flask_jwt_extended import JWTManager

load_dotenv()

app = Flask(__name__)

app.config.from_object('connection')

# JWT
app.config['JWT_SECRET_KEY'] = (
    'minha_chave_super_secreta_2026_123456'
)

# DATABASE
db = SQLAlchemy(app)

migrate = Migrate(app, db)

ma = Marshmallow(app)

api = Api(app)

# JWT MANAGER
jwt = JWTManager(app)

@jwt.unauthorized_loader
def custom_missing_jwt_callback(error):
    return jsonify({
        'message': error
    }), 401

@jwt.invalid_token_loader
def custom_invalid_token_callback(error):
    return jsonify({
        'message': error
    }), 422

@jwt.expired_token_loader
def custom_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({
        'message': 'Token expirado.'
    }), 401

# CONFIG SWAGGER
swagger_template = {

    "swagger": "2.0",

    "info": {

        "title": "API SGU",

        "description": "API Flask com JWT",

        "version": "1.0"
    },

    "securityDefinitions": {

        "Bearer": {

            "type": "apiKey",

            "name": "Authorization",

            "in": "header",

            "description":
            "Digite: Bearer {seu_token}"
        }
    },

    "security": [
        {
            "Bearer": []
        }
    ]
}

swagger = Swagger(
    app,
    template=swagger_template
)

# MODELOS
from .models.usuario_model import UsuarioModel

# VIEWS
from .views import usuario_view