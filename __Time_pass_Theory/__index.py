from fastapi import FastAPI
from models import Product, ProductUpdate

app = FastAPI() #fastAPi is a class, (web server class/FastAPI class/Uvicorn Class), and app is the object of fastAPI, so when uh creaet the objetct uh start a sever
#by createing the object of FASTAPI , uh will create a web server, or start the web server, with that app
#for stating the server uh need to mention the object name with the unvicorn server :
        # uvicorn main:app --reload  --> this app means it tells the uvicron server, that where is the server object located

@app.get("/") #this is the home route, and this app.get() function will act as the decorator
def home():
    return "This is the home page"

