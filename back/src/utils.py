import os
import uuid
from datetime import datetime, timedelta


def create_output_directory(base_path, country):
    output_dir = os.path.join(base_path, country)
    os.makedirs(output_dir, exist_ok=True)

    tomorrow_date = datetime.now() + timedelta(days=1)
    year_month_day = tomorrow_date.strftime("%Y/%m/%d")
    subdirectory = os.path.join(output_dir, year_month_day)
    os.makedirs(subdirectory, exist_ok=True)

    return subdirectory


def generate_unique_filename(extension="webp"):
    return f"{uuid.uuid4()}.{extension}"
