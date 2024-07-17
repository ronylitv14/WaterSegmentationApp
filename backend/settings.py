import os

from dotenv import load_dotenv

load_dotenv()

# Redis settings
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

# Model settings
MODEL_NAME = "UNet-water-segmentation.keras"
MODEL_FOLDER = "models"
MODEL_PATH = os.path.join(os.getcwd(), MODEL_FOLDER, MODEL_NAME)
