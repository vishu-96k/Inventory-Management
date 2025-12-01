from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
Base = declarative_base()  #this is used to map using the ORM


# this class will be converted into a tabel using the ORM
class Product(Base):
    __tablename__ = "Product"
    id = Column(Integer, primary_key=True, index=True)  #using this col fun, it will get converted into the TABLES OF ORM        
    name = Column(String)      
    description = Column(String) 
    price= Column(Integer)        
    quantity = Column(Integer)  


