from fastai.vision.all import *
import os
import zipfile
from fastapi import Body, HTTPException, Request, status, UploadFile
from model.ImageEntity import ImageEntity
from bson import ObjectId
from pymongo.collection import Collection
from schema.ImageSchema import individual_serial, list_serial


destination_folder = os.environ.get('DESTINATION_FOLDER')
model_folder = os.environ.get('MODEL_FOLDER')
learnModel: Learner = null

def get_assets_path() -> Path : 
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    return Path(destination_folder)



def get_model_path() -> Path : 
    if not os.path.exists(model_folder):
        os.makedirs(model_folder)
    return Path(model_folder)



def get_collection_images(request: Request)-> Collection:
    return request.app.database["images"]



def fill_model_with_zip(request:Request, file: UploadFile):
    print("we receive zip file")
    print(f'filename : {file.filename}')
    destination_path = get_assets_path()
    file_list = []
    with zipfile.ZipFile(file, 'r') as zip_ref:
        file_list = zip_ref.namelist()
        zip_ref.extractall(destination_path)
    
    print(f"{len(file_list)} Files extracted from '{file.filename}' and merged with '{destination_folder}'.")
    return len(file_list)+" images saved succesfully !!"



def fill_model_with_image(request:Request, file: UploadFile):
    print("Loading testing image ....")
    new_filename = saving_file_on_disk(file)
    return "Image saved succesfully !!"



def test_image(request:Request, file: UploadFile):
    print("Loading testing image ....")
    new_filename = saving_file_on_disk(file)
    
    img = PILImage.create(new_filename)
    img.to_thumb(192)
    try: 
        type, index, probs, *_ = getLearner().predict(img)
    except :
        print("we didn't predict the class of the image")
        type = "Not found"
        index = 0
        probs = [0.0]
    
    print("saving in db.")
    # Construct a new ImageEntity instance
    new_image = ImageEntity(
        name=file.filename,
        link=new_filename,
        correctness = probs[index],
        category=type, 
        createdAt=datetime.now(),
    )

    get_collection_images(request).insert_one(dict(new_image))
    return new_image



def saving_file_on_disk(file: UploadFile):
    print(f'filename : {file.filename}')
   
    new_filename = get_assets_path() / file.filename
    print(f'new_filename : {new_filename}')

    with open(new_filename, "wb") as f:
        print("file is be writing saving on disk.....")
        f.write(file.file.read())
    return new_filename



def list_images(request:Request, limit: int):
    images =  get_collection_images(request).find(limit = limit)
    return list_serial(images)



def items_labels(filename):    
    return filename[:filename.rfind('_')] 


def getLearner() :
    return load_learner(get_model_path(), cpu=True)


def delete_image(request:Request, id : str):
    deleted_image = get_collection_images(request).delete_one({"_id" : ObjectId(id) })

    print(deleted_image)
    return "Image deleted with success"

