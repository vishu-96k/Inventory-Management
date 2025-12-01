# Import BaseModel from Pydantic to create data models (schemas)
from pydantic import BaseModel

# Product model - this defines the structure of a product item
class Product(BaseModel):
    id : int              # Product ID (integer)
    name : str            # Product name (string)
    description : str     # Product description
    price : int           # Product price
    quantity : int        # How many items are available


# Import Optional, used for fields that are not mandatory
from typing import Optional

# ProductUpdate model - used for PATCH request (partial update)
class ProductUpdate(BaseModel):
    name: Optional[str] = None         # Optional → field not required
    description: Optional[str] = None
    price: Optional[int] = None
    quantity: Optional[int] = None
