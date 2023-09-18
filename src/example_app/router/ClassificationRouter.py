
from fastapi import APIRouter
from model import CategoryEntity
from fastapi import Body, HTTPException, Request, status, UploadFile
from services import ClassificationService as classificationService 
from typing import List


router = APIRouter(
    prefix="/v1/classification", tags=["Classification"]
)


@router.post("/")
def create(
    request: Request,
    word: str = Body(...)
) :
    print(f"data from the request :: {word}")
    return classificationService.create_categories(request,  [word])



@router.get("/")
def create(
    request: Request) :
    print(f"read all data from the request ")
    return classificationService.read_categories(request)



@router.post("/train-model")
def create(
    request: Request
):
    return classificationService.train_model(request)