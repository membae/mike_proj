from exts import db

"""
class Product:
    id:int primary key
    name:str
    description:str
"""

class Product(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(),nullable=False)
    description=db.Column(db.String(),nullable=False)

    def __repr__(self):
        return f"<Product {self.name}>"
    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,name,description):
        self.name=name
        self.description=description
        db.session.commit()
    


#user model
"""
class User:
    id:integer
    username:string
    email:string
    password:string
"""
class User(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    username=db.Column(db.String(255),nullable=False,unique=True)
    email=db.Column(db.String(255),nullable=False)
    password=db.Column(db.Text(),nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"