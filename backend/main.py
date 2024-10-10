from flask import Flask,request
from flask_restx import Api,Resource,fields
from config import DevConfig
from models import Product
from exts import db
from flask_migrate import Migrate

app=Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)

migrate=Migrate(app,db)

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

@api.route("/hello")
class HelloResource(Resource):
    def get(self):
        return{"message":"Hello philip,good morning"}



@api.route("/products")
class ProductsResource(Resource):
    @api.marshal_list_with(product_model)
    def get(self):
        products=Product.query.all()
        return products
    @api.marshal_with(product_model)
    def post(self):
        data=request.get_json()
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
    def put(self,id):
        product_update=Product.query.get_or_404(id)
        data=request.get_json()
        product_update.update(data.get("name"),data.get("description"))
        return product_update

    @api.marshal_with(product_model)
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