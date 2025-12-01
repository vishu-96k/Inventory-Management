#this is the configurational file for databse, uh will connect to the remote database through this file
#uh willl add the connection string, user name, and passwords in this file and then import those variables into other files

#session : everytime uh connect to something thts a session, likle if uh connect to a server thts a session, if uh connect to a database thts one session  
#to create a session, uh need to creaet a object of sessionmaker() class, and that session maker is present in the sqlalchemy, under that ORM
#uh need to pass someparameter to the object(session), nd that will be the Engine(connecgtion string whichh will connect with the actual database)
 
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url = "postgresql://postgres:root@localhost:5432/InventoryDB"  #this is the connection string 
engine = create_engine(db_url)  #helps to connect with the database, pass all the values needed to connect with database, like database name
session = sessionmaker(autocommit=False ,autoflush=False, bind=engine) #this will create a object which will coneet to DB and fetch data, so Session is noth but the database object
