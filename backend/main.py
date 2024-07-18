import os
import sys

from fastapi import status, FastAPI, UploadFile, Response, HTTPException
from keras.models import load_model
from utils.image_preprocessing import image_pipeline, save_image_to_bytes
from middlewares.cache import CachePredictionMiddleware, REQUEST_PATH

from utils.redis import save_img_prediction

app = FastAPI()

app.add_middleware(CachePredictionMiddleware)

MODEL_NAME = "UNet-water-segmentation.keras"
MODEL_FOLDER = "models"
MODEL_PATH = os.path.join(os.getcwd(), MODEL_FOLDER, MODEL_NAME)

try:
    MODEL = load_model(MODEL_PATH)
except OSError:
    sys.exit("Wrong path to model!")


@app.get("/root")
async def root():
    return {"message": "Hello World"}


@app.post(f"/{REQUEST_PATH}")
async def predict_water_segmentation(file: UploadFile):
    if "image" not in file.content_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The input must be image!"
        )

    try:
        file_data = await file.read()

        result = image_pipeline(file_data, MODEL)
        result = save_image_to_bytes(result)

        await save_img_prediction(image_bytes=file_data, image=result)

        return Response(content=result, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while processing image acquired: {e}"
        )
