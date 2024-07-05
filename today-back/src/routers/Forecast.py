import os
import logging
from datetime import datetime

from fastapi import APIRouter, Query, HTTPException
from fastapi import status
from fastapi.responses import StreamingResponse

forecast_router = APIRouter()
logger = logging.getLogger()


@forecast_router.get("/forecast", status_code=status.HTTP_200_OK)
async def get_forecast(date: str = Query(default=datetime.now().strftime("%Y/%m/%d")),
                       country: str = Query(default="spain")):
    try:
        # Parse the date string
        date_obj = datetime.strptime(date, "%Y/%m/%d")

        # Format the directory path
        dir_path = os.path.join(country, str(date_obj.year), str(date_obj.month).zfill(2), str(date_obj.day).zfill(2))

        # Check if directory exists
        if not os.path.isdir(dir_path):
            raise HTTPException(status_code=404, detail="Image directory not found for the specified date and country")

        # List files in the directory
        files_in_dir = os.listdir(dir_path)

        # Check if there are files in the directory
        if not files_in_dir:
            raise HTTPException(status_code=404, detail="No image files found for the specified date and country")

        # Get the first file in the directory
        first_file = files_in_dir[0]
        image_path = os.path.join(dir_path, first_file)

        # Return the image as a streaming response
        return StreamingResponse(open(image_path, 'rb'), media_type='image/webp')

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use YYYY/MM/DD.")
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=500, detail="An error occurred while processing the request")