from flask_restx import Namespace,Resource,fields
from models import Product
from flask_jwt_extended import jwt_required
from flask import request

product_ns=Namespace('product',description='A namespace for products')


product_model=product_ns.model(
    "Product",
    {
        "id":fields.Integer(),
        "name":fields.String(),
        "description":fields.String()
    }
)





@product_ns.route("/hello")
class HelloResource(Resource):
    def get(self):
        return{"message":"Hello philip,good morning"}





        


    



@product_ns.route("/products")
class ProductsResource(Resource):
    @product_ns.marshal_list_with(product_model)
    def get(self):
        products=Product.query.all()
        return products
    
    @product_ns.marshal_with(product_model)
    @product_ns.expect(product_model)
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


@product_ns.route("/products/<int:id>")
class ProductResource(Resource):
    @product_ns.marshal_with(product_model)
    def get(self,id):
        product=Product.query.get_or_404(id)
        return product

    @product_ns.marshal_with(product_model)
    @jwt_required()
    def put(self,id):
        product_update=Product.query.get_or_404(id)
        data=request.get_json()
        product_update.update(data.get("name"),data.get("description"))
        return product_update

    @product_ns.marshal_with(product_model)
    @jwt_required()
    def delete(self,id):
        product_to_delete=Product.query.get_or_404(id)
        product_to_delete.delete()
        return product_to_delete
