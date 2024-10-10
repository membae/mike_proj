from flask import Flask,request,jsonify
from flask_restx import Api,Resource,fields
from config import DevConfig
from models import Product,User
from exts import db
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt_extended import JWTManager,create_access_token,create_refresh_token,jwt_required

app=Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

migrate=Migrate(app,db)
JWTManager(app)

api=Api(app,doc="/docs")

#model (serializer)
product_model=api.model(
    "Product",
    {
        "id":fields.Integer(),
        "name":fields.String(),
        "description":fields.String()
    }
)

signup_model=api.model(
    "SignUp",
    {
       'username':fields.String(),
       'email':fields.String(),
       'password':fields.String()
    }
)

login_model=api.model(
    'Login',
    {
        "username":fields.String(),
        "password":fields.String()
    }
)



@api.route("/hello")
class HelloResource(Resource):
    def get(self):
        return{"message":"Hello philip,good morning"}

@api.route("/signup")
class SignUp(Resource):
    # @api.marshal_with(signup_model)
    @api.expect(signup_model)
    def post(self):
        data=request.get_json()

        username=data.get("username")
        db_user=User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify({"message":f"user with username {username} already exists"})

        new_user=User(
            username=data.get("username"),
            email=data.get("email"),
            password=generate_password_hash(data.get('password'))
        )

        new_user.save()
        return jsonify({"message":"user creayed successfully"})
    




        

@api.route("/login")
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        data=request.get_json()
        username=data.get("username")
        password=data.get("password")
        
        db_user=User.query.filter_by(username=username).first()

        if db_user and check_password_hash(db_user.password,password):
            access_token=create_access_token(identity=db_user.username)
            refresh_token=create_refresh_token(identity=db_user.username)

            return jsonify(
                {"access_token":access_token,"refresh_token":refresh_token}
            )

    



@api.route("/products")
class ProductsResource(Resource):
    @api.marshal_list_with(product_model)
    def get(self):
        products=Product.query.all()
        return products
    
    @api.marshal_with(product_model)
    @api.expect(product_model)
    @jwt_required
    def post(self):
        data=request.get_json()
        if not data:
            return {"message": "No input data provided"}, 400
        
        new_product=Product(
            name=data.get("name"),
            description=data.get("description")
        )
        new_product.save()
        return new_product,201


@api.route("/products/<int:id>")
class ProductResource(Resource):
    @api.marshal_with(product_model)
    def get(self,id):
        product=Product.query.get_or_404(id)
        return product

    @api.marshal_with(product_model)
    @jwt_required()
    def put(self,id):
        product_update=Product.query.get_or_404(id)
        data=request.get_json()
        product_update.update(data.get("name"),data.get("description"))
        return product_update

    @api.marshal_with(product_model)
    @jwt_required()
    def delete(self,id):
        product_to_delete=Product.query.get_or_404(id)
        product_to_delete.delete()
        return product_to_delete

@app.shell_context_processor
def make_shell_context():
    return {
        "db":db,
        "Product":Product
    }





if __name__=="__main__":
    app.run()