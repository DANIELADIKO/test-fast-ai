
from fastapi import APIRouter


from model import ImageEntity
from fastapi import Body, HTTPException, Request, status, UploadFile
from services import ImageService as imagesService 
from typing import List


router = APIRouter(
    prefix="/v1/images", tags=["Image"]
)


@router.post("/test-image", response_description="Test image classification", status_code= status.HTTP_201_CREATED)
def test_image(
    request: Request,
    file: UploadFile
) :
    return imagesService.create_image(request, file)


@router.get("/")
def getAll(request: Request, limit: int = 20):
    return imagesService.list_images(request, limit)

