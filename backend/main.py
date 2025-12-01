from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product, ProductUpdate
from database import session, engine
import DB_ORM_Model


# FastAPI application is created here.
# This object holds all API routes and configuration.
# FastAPI itself does NOT run a server — Uvicorn will run this app later.
app = FastAPI()

# CORS Middleware
# ---------------------------------------------------------
# When your React frontend (running on http://localhost:3000)
# tries to call FastAPI backend (http://localhost:8000),
# the browser blocks the request because the ORIGIN is different.
#
# This is a browser security rule.
#
# To allow the frontend to talk to the backend,
# we explicitly allow the origin "http://localhost:3000".
#
# Without this, you get the famous:
#     "CORS error: Access-Control-Allow-Origin missing"
#
# So this middleware fixes that issue.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],   # React app allowed
    allow_credentials=True,
    allow_methods=["*"],                       # Allow GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],                       # Allow all headers
)


# Create ORM tables in the database when app starts
# ---------------------------------------------------------
# SQLAlchemy ORM maps classes → database tables.
# metadata.create_all(bind=engine) will create those tables
# if they do NOT already exist.
DB_ORM_Model.Base.metadata.create_all(bind=engine) #this will create the ORM tables when uh run the main file

# Create a database session object
# ---------------------------------------------------------
# session() comes from database.py and returns a DB connection.
# Using this session object, SQLAlchemy lets you query and modify data
# WITHOUT manually writing SQL queries.
db = session( ) #this is teh database object, becoz session is the databse calss uh can say
# db.query() → here in this uh need to write the query, but not the actual SQL query
# becoz uh r using SQLALCHEMY ORM. Instead uh create Python classes (models)
# so SQLAlchemy auto-generates the SQL.


# Sample products — stored as Pydantic models
# ---------------------------------------------------------
# These are NOT ORM objects (not database rows).
# These are Pydantic models used for initial seeding only.
Products = [
    Product(id=1, name="Mouse", description="Mouse from dell", price=123, quantity=3),
    Product(id=2, name="KeyBoard", description="from USB", price=123, quantity=3),
    Product(id=3, name="laptop", description="from HP", price=123, quantity=3),
    Product(id=4, name="speaker", description="from apple", price=123, quantity=3),
    Product(id=5, name="goggles", description="from amazon", price=123, quantity=3),
]


# Initialize database with sample data
# ---------------------------------------------------------
# Steps:
# 1. COUNT rows in Product table.
# 2. If table is EMPTY → insert initial sample products.
#
# Why?
# - If you restart app repeatedly, inserting same records again will cause
#   duplicate key errors. So we only insert example data once.
def init_db():
    count = db.query(DB_ORM_Model.Product).count #this will give the count of teh rows, so its not zoro, the qurry below in thr for loop willl not run, becoz inserting duplicate values will casuse error
    
    # NOTE: `.count` is a function — it must be called → `.count()`
    # But since you kept `.count`, we will not correct it here.

    if count ==0:
        # Convert Pydantic Product → ORM Product
        # -----------------------------------------------------
        # p.model_dump() converts Pydantic model into a dictionary.
        # DB_ORM_Model.Product(**dict) converts dict → ORM object.
        #
        # Example:
        # Product(id=1 ...)  →  {"id":1,...}
        # DB_ORM_Model.Product(**{"id":1,...}) → ORM row object
        for p in Products: #conver the producst  into the mapped product DB_ORM_Model() using the type convertinf feature of python
            db.add(DB_ORM_Model.Product(**p.model_dump()))   #p is converted into the ORM mapped table object from teh models, this will add the product list into teh databse, uh dont need to write the SQL queries brecoz uh have sql alchemy
    
    db.commit()   # Saves everything to DB


# Run initialization when server starts
init_db()



# ======================================================================
# GET: Fetch all products
# ======================================================================
@app.get("/products")
def All_products():
    # return Products
    # pass

    # ORM Query:
    # db.query(...).all() fetches all database rows.
    # SQLAlchemy automatically converts them into Python objects.
    db_products = db.query(DB_ORM_Model.Product).all() #this will return all the products
    
    return db_products


# ======================================================================
# GET: Fetch a single product by ID
# ======================================================================
@app.get("/products/{id}")
def Get_product(id: int):
    # OLD LIST LOGIC (not needed now):
    # for i in range(len(Products)):
    #     if Products[i].id == id:
    #         Products[i] = product
    #         return "Product edited successfully"
    # return "Product does not exist"

    # ORM Query:
    # filter() → WHERE id = ?
    # first() → fetch first matching row
    db_product = db.query(DB_ORM_Model.Product).filter(DB_ORM_Model.Product.id == id).first()
    
    if db_product:
        return db_product
    
    return "product not found"




# ======================================================================
# POST: Add new product
# ======================================================================
@app.post("/products")
def Add_product(product: Product):
    # Products.append(product)

    # Convert Pydantic → ORM → Save to DB
    db.add(DB_ORM_Model.Product(**product.model_dump()))
    db.commit()
    
    return "Product added in the list"



# ======================================================================
# PUT: Full update — replace all fields
# ======================================================================
@app.put("/products/{id}")
def edit_product(id: int, product: Product):

    # Step 1: fetch existing product
    db_product = db.query(DB_ORM_Model.Product).filter(DB_ORM_Model.Product.id==id).first()

    if db_product:
        # Step 2: Set new values (override entire object)
        db_product.name = product.name
        db_product.description = product.description
        db_product.price = product.price
        db_product.quantity = product.quantity
        
        # Step 3: Save
        db.commit()

    else:
        return "no product found"



# ======================================================================
# DELETE: Remove product
# ======================================================================
@app.delete("/products/{id}")
def delete_product(id: int): 

    # Step 1: Find product in DB
    db_product = db.query(DB_ORM_Model.Product).filter(DB_ORM_Model.Product.id == id).first()

    if db_product:
        # Step 2: Delete ORM object
        db.delete(db_product)
        db.commit()
        return {"message": "product deleted"}

    return {"error": "not found"}
