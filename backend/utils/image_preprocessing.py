import io

import numpy as np
from io import BytesIO
import tensorflow as tf
from keras.preprocessing.image import load_img, img_to_array, array_to_img

IMG_HEIGHT = 224
IMG_WIDTH = 224


def read_image(img):
    img = BytesIO(img)
    img = load_img(img)
    img = img_to_array(img)
    img = tf.image.resize(img, (IMG_HEIGHT, IMG_WIDTH))
    return img / 255.


def overlay_mask_on_image(img, mask, alpha=0.5, mask_measure=0.4):
    mask_rgb = np.where(mask > mask_measure, [1, 1, 0], [0, 0, 0])
    overlay = np.clip(img + mask_rgb * alpha, 0, 1)
    return overlay


def get_model_prediction(img, model):
    batched_img = np.expand_dims(img, axis=0)
    prediction = model.predict(batched_img)
    return prediction[0]


def image_pipeline(file_data, model):
    img = read_image(file_data)
    mask = get_model_prediction(img, model)
    result = overlay_mask_on_image(img, mask, alpha=0.4, mask_measure=0.3)
    return array_to_img(result)


def save_image_to_bytes(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    return img_byte_arr.read()
