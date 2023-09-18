from fastai.vision.all import *
import os
from fastapi import Body, HTTPException, Request, status, UploadFile
from model import ImageEntity
from bson import ObjectId
from pymongo.collection import Collection
from schema.ImageSchema import individual_serial, list_serial

destination_folder = os.environ.get('DESTINATION_FOLDER')
learnModel: Learner = null

def get_assets_path() -> Path : 
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    return Path(destination_folder)

def get_collection_images(request: Request)-> Collection:
    return request.app.database["images"]


def create_image(request:Request, file: UploadFile):
    print("Loading saving image ....")
    print(f'filename : {file.filename}')
   
    new_filename = get_assets_path() / file.filename
    with open(new_filename, "wb") as f:
        print("file is be writing saving on disk.....")
        f.write(file.file.read())
    
    img = PILImage.create(new_filename)
    img.to_thumb(192)
    try: 
        type, index, probs, *_ = learnModel.predict(img)
    except :
        print("we didn't predict the class of the image")
        type = "Not found"
        index = 0
        probs = [0.0]
    
    print("saving in db.")

    created_at = datetime.now()

     # Construct a new ImageEntity instance
    new_image = ImageEntity(
        name=file.filename,
        link=new_filename,
        correctness = probs[index],
        category=type, 
        createdAt=created_at,
    )

    get_collection_images(request).insert_one(dict(new_image))
    return new_image

       
    
def list_images(request:Request, limit: int):
    images =  get_collection_images(request).find(limit = limit)
    return list_serial(images)



def delete_image(request:Request, id : str):
    deleted_image = get_collection_images(request).delete_one({"_id" : ObjectId(id) })

    print(deleted_image)
    return "Image deleted with success"

