import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Path, status
from httpx import Response
from fastai.vision.all import *

# app
app: FastAPI = FastAPI()

learnModel: Learner

# method to train model with path of images
def trainModel(path):
    dls = ImageDataLoaders.from_name_func(
        path,
        get_image_files(path),
        valid_pct = 0.25,
        seed = 42,
        label_func = items_labels,
        item_tfms = Resize(224))
    
    print("All Category recorded in the model :: ")
    for vocab in dls.vocab:
        print(vocab)

    #train model
    learn = vision_learner(dls, resnet34, metrics = error_rate)
    #refine model
    learn.fine_tune(1)
    return learn

# method to take category from model
def items_labels(filename):    
    return filename[:filename.rfind('_')]  


@app.get(path="/", status_code=status.HTTP_200_OK)
def get_img_category() -> dict :

    img = PILImage.create('beagle-hound-dog.webp')
    img.to_thumb(192)
    animal_type, index, probs = learnModel.predict(img)

    return { 'category' : animal_type , "percent" :  probs[index] }


@app.get(path="/{chemin}", status_code=status.HTTP_200_OK)
def start_trainning(chemin: str) -> str :
    learnModel = trainModel(chemin)
    return 'model trainning finished'



if __name__ == "__main__":
    uvicorn.run(app="app:app", host="127.0.0.1", port=9000, reload=True)




#  1- charger uneliste d'image
# 2- les images doivent etre nommés au format categorie_1, categorie_2 : ex : coca_cola_1