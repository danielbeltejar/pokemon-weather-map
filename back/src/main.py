import json
import os
from time import sleep

from dotenv import load_dotenv
from src.constants import COUNTRIES_LIST, POKEMONS, TEMPERATURE_RANGES, TESTING
from src.logger import setup_logger
from src.image_filler import ImageFiller
from src.utils import create_output_directory, generate_unique_filename

load_dotenv()


def main():
    logger = setup_logger()

    for country in COUNTRIES_LIST:
        try:
            with open(f"config/{country}.json", "r", encoding="utf-8") as file:
                provinces = json.load(file)

            image_filler = ImageFiller(
                image_path=f"images/{country}.png",
                pokemons=POKEMONS,
                temperature_ranges=TEMPERATURE_RANGES,
                logger=logger,
                testing=TESTING,
                country=country,
                provinces=provinces
            )

            success = False
            while not success:
                try:
                    image_filler.fill_image()
                    success = True
                except Exception as e:
                    logger.error(f"Error processing {country}: {e}")
                    sleep(300)

            output_dir = create_output_directory("images/output", country)
            file_path = os.path.join(output_dir, generate_unique_filename())
            image_filler.save_image(file_path)
            image_filler.generate_ai_forecast()

        except Exception as e:
            logger.error(f"Critical error with {country}: {e}")


if __name__ == "__main__":
    main()
