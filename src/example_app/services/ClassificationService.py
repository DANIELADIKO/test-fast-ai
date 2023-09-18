from fastai.vision.all import *
import os
from fastapi import Body, HTTPException, Request
from model.CategoryEntity import CategoryEntity
from bson import ObjectId
from pymongo.collection import Collection
from typing import List
from schema.CategorySchema import individual_serial, list_serial


destination_folder = os.environ.get('DESTINATION_FOLDER')
learnModel: Learner = null


def get_assets_path() -> Path : 
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    return Path(destination_folder)



def get_collection_category(request: Request) -> Collection:
    return request.app.database["category"]




def read_categories(request: Request):
    collection = get_collection_category(request)
    all_items = collection.find()
    return list_serial(all_items)




def create_categories(request: Request, word_list : List[str]):
    collection = get_collection_category(request)

    existing_categories = set(
        category["name"]
        for category in collection.find({}, {"name": 1})
    )
    
    new_categories = []
    
    for word in word_list:
        if word not in existing_categories:
            created_at = datetime.now()
            new_category = CategoryEntity(
                name=word,
                createdAt=created_at,
            )
            new_categories.append(new_category)
    
    print(f"new categories :: {new_categories}")
    if new_categories:
        result = collection.insert_many([dict(newcat) for newcat in new_categories])
        # Use the inserted_ids to retrieve the newly added documents
        cursor = collection.find({"_id": {"$in": result.inserted_ids}})

        new_categories = [category for category in cursor]
        # Return the new categories as JSON
        return list_serial(new_categories)
    else:
        print("No new categories to add.")
        return []




def train_model(request: Request): 
    print("start train model method ...")
    path = get_assets_path()
    print(f"---- where to find images :: {path}")
    dls = ImageDataLoaders.from_name_func(
        path,
        get_image_files(path),
        valid_pct = 0.25,
        seed = 42,
        label_func = items_labels,
        item_tfms = Resize(224))
    
    new_vocab = []
    for vocab in dls.vocab:
        new_vocab.append(vocab)
    
    create_categories(request, new_vocab)

    print("Start Vision learn -----")
    learnModel = vision_learner(dls, resnet34, metrics = error_rate)
    #refine model
    print("Start Refine Model -----")
    learnModel.fine_tune(1)



def items_labels(filename):    
    return filename[:filename.rfind('_')]  
