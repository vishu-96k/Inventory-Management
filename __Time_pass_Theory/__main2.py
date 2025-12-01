# Import FastAPI class from the fastapi package.
# ---------------------------------------------------------
# FastAPI is a CLASS that helps you create a web application.
# When we create an object of FastAPI(), we get an ASGI application.
# ASGI = Asynchronous Server Gateway Interface (modern version of WSGI)
#
# FastAPI DOES NOT run a server by itself.
# It only CREATES the app object.
# The server is actually started by uvicorn:
#       uvicorn main:app --reload
#
# FastAPI internally:
#   - Registers routes (GET/POST/PUT/DELETE)
#   - Validates incoming data using Pydantic
#   - Converts responses to JSON
#   - Generates Swagger API docs automatically
from fastapi import FastAPI


# Import Product and ProductUpdate models from models.py
# ---------------------------------------------------------
# These are Pydantic models (classes) that define the STRUCTURE of data.
# Product → used when creating a new product or full update (PUT)
# ProductUpdate → used for partial update (PATCH), so fields are optional
#
# FastAPI uses these models to:
#   - Validate incoming JSON request bodies
#   - Ensure correct data types (int, str, etc.)
#   - Automatically generate schema in Swagger docs
from models import Product, ProductUpdate


# Create the FastAPI application instance
# ---------------------------------------------------------
# app = FastAPI() creates an "application object".
#
# IMPORTANT:
# This DOES NOT start a server.
#
# It only PREPARES the FastAPI app:
#   - This object stores all routes you define with @app.get, @app.post, etc.
#   - It behaves like a "manager" of your whole API.
#
# The actual server is started with Uvicorn which loads this 'app':
#   uvicorn main:app --reload
#
# When Uvicorn runs, it uses this 'app' object to:
#   - Handle incoming HTTP requests
#   - Match URLs to route functions
#   - Run your code
#   - Return JSON responses
app = FastAPI()



# -----------------------------------------------------------------------
# IN-MEMORY DATABASE
# Here we are storing products in a Python list.
# In a real app, this would be a database like MongoDB, MySQL, PostgreSQL.
# -----------------------------------------------------------------------
Products = [
    Product(id=1,name="Mouse", description="Mouse from dell", price=123, quantity=3),
    Product(id=2,name="KeyBoard", description="from USB", price=123, quantity=3),
    Product(id=3,name="laptop", description="from HP", price=123, quantity=3),
    Product(id=4,name="speaker", description="from apple", price=123, quantity=3),
    Product(id=5,name="goggles", description="from amazon", price=123, quantity=3),
]


# =======================================================================
# GET API → Home Route
# =======================================================================
@app.get("/")
def home():
    # When user visits root URL "/" → this message is returned.
    return "This is the home page"


# =======================================================================
# GET API → Fetch All Products
# =======================================================================
@app.get("/products")
def products_get():
    # This returns the entire product list.
    # FastAPI automatically converts Product objects → JSON.
    return Products


# =======================================================================
# POST API → Add a New Product
# =======================================================================
@app.post("/Products")
def Add_product(product: Product):
    """
    This API:
    - Accepts a new product as input (validated by Product model)
    - Appends it to our Products list
    - Returns success message
    """
    Products.append(product)
    return "Product added in the list"


# =======================================================================
# PUT API → Full Update
# =======================================================================
@app.put("/products/{id}")
def Edit_products(id: int, product: Product):
    """
    PUT = FULL UPDATE
    - You must send ALL fields (id, name, description, price, quantity)
    - This replaces the entire old product with the new one
    """

    # Loop through list using index (so we can replace item)
    for i in range(len(Products)):

        # Check if product with given ID exists
        if Products[i].id == id:
            
            # Replace old product object with new product object
            Products[i] = product
            return "Product edited successfully"

    # If no matching ID found
    return "Product does not exist"


# =======================================================================
# PATCH API → Partial Update
# =======================================================================
@app.patch("/products/{id}")
def edit_product(id: int, update: ProductUpdate):
    """
    PATCH = PARTIAL UPDATE
    - User sends only the fields they want to update
    - Example: { "price": 999 }
    - Other fields remain unchanged
    """

    # Loop through all products
    for product in Products:

        # Match product by ID
        if product.id == id:

            # Convert update fields to dict
            # exclude_unset=True = only include fields user sent
            update_data = update.dict(exclude_unset=True)

            # Update only provided fields
            for key, value in update_data.items():
                setattr(product, key, value)  # Example: product.price = 999

            return product  # Return updated product object

    # No matching product found
    return {"error": "Product not found"}


# =======================================================================
# DELETE API → Delete a Product
# =======================================================================
@app.delete("/delete/{id}")
def delete_product(id: int):
    """
    This API:
    - Searches for a product with matching ID
    - Removes it from the list
    - Returns success/failure message
    """

    for product in Products:

        # If product is found
        if product.id == id:
            Products.remove(product)  # Delete the product
            return "Product deleted successfully"

    # If ID does not exist
    return "Product not found"
