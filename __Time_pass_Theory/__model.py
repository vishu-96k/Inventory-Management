#model : this is a data representation, model holds data
#if uh want to hold data for user, products, then this is a 2 diff models
#Using the ORM (object relation mappping), the model (data classes) will be getting converted into tables of SQL
#one model represents one Table.
#ClASS NAME = TABLE name
#CLASS DATA MEMBERS = COLUMNS NAMES
#Objects of class = Actaul data feilds of the tables

#EG :

class Prodcut:
    id : int
    name : str
    description : str
    quantity : int

#PYDANTIC 
#it helps for data validation.

#BASEMODEL : this is a class in pydantic library, and it helps for data validations
#so uh need to inhirt the BaseModel class into the Models (data classes)