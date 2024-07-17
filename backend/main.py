import os
import sys

from fastapi import status, FastAPI, UploadFile, Response, HTTPException
from keras.models import load_model
from utils.image_preprocessing import image_pipeline, save_image_to_bytes

app = FastAPI()

MODEL_NAME = "UNet-water-segmentation.keras"
MODEL_FOLDER = "models"
MODEL_PATH = os.path.join(os.getcwd(), MODEL_FOLDER, MODEL_NAME)

try:
    MODEL = load_model(MODEL_PATH)
except OSError:
    sys.exit("Wrong path to model!")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/predict")
async def predict_water_segmentation(file: UploadFile):
    try:
        file_data = await file.read()

        result = image_pipeline(file_data, MODEL)
        result = save_image_to_bytes(result)

        return Response(content=result, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error while processing image acquired: {e}"
        )
