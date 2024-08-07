import sys

from fastapi import status, FastAPI, UploadFile, Response, HTTPException
from keras.models import load_model
from utils.image_preprocessing import image_pipeline, save_image_to_bytes

from middlewares.cache import CachePredictionMiddleware, REQUEST_PATH
from middlewares.rate_limiting import RateLimitingMiddleware
from fastapi.middleware.cors import CORSMiddleware

from utils.redis import save_img_prediction

from settings import MODEL_PATH

app = FastAPI()

origins = [
    "http://localhost:9000",
]

app.add_middleware(CachePredictionMiddleware)
app.add_middleware(RateLimitingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

try:
    MODEL = load_model(MODEL_PATH)
except OSError:
    sys.exit("Wrong path to model!")


@app.get("/")
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
