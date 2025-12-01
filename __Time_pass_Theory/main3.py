from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product, ProductUpdate
from database import session, engine
import DB_ORM_Model


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_ORM_Model.Base.metadata.create_all(bind=engine) #this will create the ORM tables when uh run the main file
db = session( ) #this is teh database object, becoz session is the databse calss uh can say
# db.query()  here in this uh need to write the query, but not the actual query becoz uh r using SQLALCHEMY
                #uh need to create teh database scehema using class, so that the alchemy can map it with ORM



Products = [
    Product(id=1, name="Mouse", description="Mouse from dell", price=123, quantity=3),
    Product(id=2, name="KeyBoard", description="from USB", price=123, quantity=3),
    Product(id=3, name="laptop", description="from HP", price=123, quantity=3),
    Product(id=4, name="speaker", description="from apple", price=123, quantity=3),
    Product(id=5, name="goggles", description="from amazon", price=123, quantity=3),
]

def init_db():
    count = db.query(DB_ORM_Model.Product).count #this will give the count of teh rows, so its not zoro, the qurry below in thr for loop willl not run, becoz inserting duplicate values will casuse error
    if count ==0:
     
        for p in Products: #conver the producst  into the mapped product DB_ORM_Model() using the type convertinf feature of python
            db.add(DB_ORM_Model.Product(**p.model_dump()))   #p is converted into the ORM mapped table object from teh models, this will add the product list into teh databse, uh dont need to write the SQL queries brecoz uh have sql alchemy
    db.commit()

init_db()

  

@app.get("/products")
def All_products():
    # return Products
    # pass
    db_products = db.query(DB_ORM_Model.Product).all() #this will return all the products
    return db_products


@app.get("/products/{id}")
def Get_product(id: int):
    # for i in range(len(Products)):
    #     if Products[i].id == id:
    #         Products[i] = product
    #         return "Product edited successfully"
    # return "Product does not exist"
    db_product = db.query(DB_ORM_Model.Product).filter(DB_ORM_Model.Product.id == id).first()
    if db_product:
        return db_product
    return "product not found"





@app.post("/products")
def Add_product(product: Product):
    # Products.append(product)
    db.add(DB_ORM_Model.Product(**product.model_dump()))
    db.commit()
    return "Product added in the list"


@app.put("/products/{id}")
def edit_product(id: int, product: Product):
    db_product =db.query(DB_ORM_Model.Product).filter(DB_ORM_Model.Product.id==id).first()
    if db_product:
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        db.commit()
    else:return "no product found"

@app.delete("/products/{id}")
def delete_product(id: int): 
    db_product = db.query(DB_ORM_Model.Product).filter(DB_ORM_Model.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": "product deleted"}

    return {"error": "not found"}
