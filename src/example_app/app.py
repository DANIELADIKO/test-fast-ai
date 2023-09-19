from fastapi import FastAPI
from router import ImageRouter, ClassificationRouter
from pymongo import MongoClient
from dotenv import load_dotenv
import uvicorn
import os 


load_dotenv('.env')


destination_folder = os.environ.get('DESTINATION_FOLDER')
db_url = os.environ.get('DB_URL')
db_name = os.environ.get('DB_NAME')

# app
app: FastAPI = FastAPI()

@app.on_event("startup")
def startup_db_client():
    print(f"DB URL : {db_url} / {db_name}")
    app.mongodb_client = MongoClient(db_url)
    app.database = app.mongodb_client[db_name]
    try : 
        app.database.command('ping')
        print("project connected to database  !!")
    except Exception as e :
        print(f"error trying to connect to db : {e}") 
    
    


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close() 
    print("project disconnectedd from database  !!")


app.include_router(ImageRouter.router)
app.include_router(ClassificationRouter.router)



if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=9000, reload=True)


