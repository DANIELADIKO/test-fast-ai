
from fastapi import APIRouter
from model.ImageEntity import ImageEntity
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
    return imagesService.test_image(request, file)



@router.post("/upload-image", response_description="Upload image in the model trainning dataset", status_code= status.HTTP_201_CREATED)
def upload_image(
    request: Request,
    file: UploadFile
) :
    return imagesService.fill_model_with_image(request, file)



@router.post("/upload-zip", response_description="Upload image in the model trainning dataset", status_code= status.HTTP_201_CREATED)
def upload_image(
    request: Request,
    file: UploadFile
) :
    return imagesService.fill_model_with_zip(request, file)



@router.get("/")
def getAll(request: Request, limit: int = 20) -> List[ImageEntity]:
    return imagesService.list_images(request, limit)

