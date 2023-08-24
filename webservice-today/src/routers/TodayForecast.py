import os
import logging
from datetime import datetime

from fastapi import APIRouter
from fastapi import status
from fastapi.responses import StreamingResponse

today_forecast_router = APIRouter()
logger = logging.getLogger()

base_image_directory = 'spain'


@today_forecast_router.get('/forecast/today', status_code=status.HTTP_200_OK)
def today_forecast():
    try:
        today_date = datetime.now()

        dir_path = os.path.join(base_image_directory, str(today_date.year),
                                str(today_date.month).zfill(2), str(today_date.day).zfill(2))

        if not os.path.isdir(dir_path):
            return {"error": "Image directory not found for today's date"}

        files_in_dir = os.listdir(dir_path)

        if not files_in_dir:
            return {"error": "No image files found for today's date"}

        first_file = files_in_dir[0]

        image_path = os.path.join(dir_path, first_file)

        return StreamingResponse(open(image_path, 'rb'), media_type='image/webp')

    except Exception as e:
        logger.error(str(e))
        return {"error": "An error occurred while processing the request"}
