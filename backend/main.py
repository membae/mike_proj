from flask import Flask
from flask_restx import Api

from models import Product,User
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from products import product_ns
from auth import auth_ns


def create_app(config):
    app=Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    migrate=Migrate(app,db)
    JWTManager(app)

    api=Api(app,doc="/docs")

    api.add_namespace(product_ns)
    api.add_namespace(auth_ns)

    #model (serializer)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db":db,
            "Product":Product,
            "user":User
        }
    
    return app





