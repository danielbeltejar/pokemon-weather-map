import json
import os
import uuid
from datetime import datetime, timedelta
from time import sleep

from dotenv import load_dotenv

from ImageFiller import ImageFiller

load_dotenv()
testing = bool(os.getenv("DEBUG")) if os.getenv("DEBUG") else False
countries_list = ["spain", "unitedstates"]

pokemons = {
    "hot": "Charmander",
    "hotter": "Charmeleon",
    "hottest": "Charizard",
    "frozen": "Regice",
    "rain": "Castform_rainy",
    "drizzle": "Castform_rainy",
    "hail": "Avalugg",
    "snow": "Articuno",
    "thunderstorm": "Zapdos",
    "clear": "Solrock",
    "sunny": "Solrock",
    "cloudy": "Togekiss",
    "partly cloudy": "Castform",
    "overcast": "Togekiss",
    "mist": "Gengar",
    "fog": "Gengar",
    "freezing fog": "Gengar",
    "patchy rain nearby": "Castform_rainy",
    "patchy rain possible": "Castform_rainy",
    "patchy light drizzle": "Castform_rainy",
    "light rain shower": "Castform_rainy",
    "moderate rain at times": "Castform_rainy",
    "heavy rain at times": "Castform_rainy",
    "moderate or heavy rain shower": "Castform_rainy",
    "patchy light snow": "Articuno",
    "light snow": "Articuno",
    "light snow showers": "Articuno",
    "patchy heavy snow": "Articuno",
    "moderate or heavy snow showers": "Articuno",
    "moderate or heavy snow in area with thunder": "Articuno",
    "patchy snow nearby": "Articuno",
    "light sleet showers": "Articuno",
    "moderate or heavy sleet showers": "Articuno",
    "light showers of ice pellets": "Avalugg",
    "thundery outbreaks in nearby": "Zapdos",
    "patchy light rain in area with thunder": "Zapdos",
    "patchy light snow in area with thunder": "Zapdos",
    "light rain": "Castform_rainy",
    "light drizzle": "Castform_rainy",
    "patchy light rain": "Castform_rainy",
    "moderate rain": "Castform_rainy",
    "heavy rain": "Castform_rainy",
    "torrential rain shower": "Castform_rainy",
    "blowing snow": "Articuno",
    "moderate or heavy sleet": "Articuno",
    "blizzard": "Articuno",
    "patchy moderate snow": "Articuno",
    "moderate snow": "Articuno",
    "heavy snow": "Articuno",
    "patchy sleet nearby": "Articuno",
    "patchy freezing drizzle nearby": "Castform_rainy",
    "freezing drizzle": "Articuno",
    "heavy freezing drizzle": "Articuno",
    "light freezing rain": "Articuno",
    "moderate or heavy freezing rain": "Articuno",
    "light sleet": "Articuno",
    "ice pellets": "Avalugg",
    "moderate or heavy showers of ice pellets": "Avalugg",
    "moderate or heavy rain in area with thunder": "Avalugg"
}

temperature_ranges = [
    {"range": (-100.0, 0.0), "color": (135, 206, 250, 255)},
    {"range": (-10.0, -9.0), "color": (135, 206, 250, 255)},
    {"range": (-9.0, -8.0), "color": (137, 205, 247, 255)},
    {"range": (-8.0, -7.0), "color": (140, 204, 245, 255)},
    {"range": (-7.0, -6.0), "color": (143, 204, 242, 255)},
    {"range": (-6.0, -5.0), "color": (146, 203, 240, 255)},
    {"range": (-5.0, -4.0), "color": (149, 203, 237, 255)},
    {"range": (-4.0, -3.0), "color": (151, 202, 235, 255)},
    {"range": (-3.0, -2.0), "color": (154, 201, 232, 255)},
    {"range": (-2.0, -1.0), "color": (157, 201, 230, 255)},
    {"range": (-1.0, 0.0), "color": (160, 200, 227, 255)},
    {"range": (0.0, 1.0), "color": (163, 200, 225, 255)},
    {"range": (1.0, 2.0), "color": (167, 206, 227, 255)},
    {"range": (2.0, 3.0), "color": (171, 212, 229, 255)},
    {"range": (3.0, 4.0), "color": (173, 216, 230, 255)},
    {"range": (4.0, 5.0), "color": (174, 218, 229, 255)},
    {"range": (5.0, 6.0), "color": (175, 221, 228, 255)},
    {"range": (6.0, 7.0), "color": (176, 223, 228, 255)},
    {"range": (7.0, 8.0), "color": (176, 223, 229, 255)},
    {"range": (8.0, 9.0), "color": (176, 224, 230, 255)},
    {"range": (9.0, 10.0), "color": (185, 228, 231, 255)},
    {"range": (10.0, 11.0), "color": (194, 232, 233, 255)},
    {"range": (11.0, 12.0), "color": (199, 234, 234, 255)},
    {"range": (12.0, 13.0), "color": (209, 242, 242, 255)},
    {"range": (13.0, 14.0), "color": (219, 250, 250, 255)},
    {"range": (14.0, 15.0), "color": (224, 255, 255, 255)},
    {"range": (15.0, 16.0), "color": (208, 249, 216, 255)},
    {"range": (16.0, 17.0), "color": (192, 244, 178, 255)},
    {"range": (17.0, 18.0), "color": (185, 242, 159, 255)},
    {"range": (18.0, 19.0), "color": (168, 240, 153, 255)},
    {"range": (19.0, 20.0), "color": (152, 238, 147, 255)},
    {"range": (20.0, 21.0), "color": (144, 238, 144, 255)},
    {"range": (21.0, 22.0), "color": (86, 244, 86, 255)},
    {"range": (22.0, 23.0), "color": (28, 251, 28, 255)},
    {"range": (23.0, 24.0), "color": (0, 255, 0, 255)},
    {"range": (24.0, 25.0), "color": (20, 235, 20, 255)},
    {"range": (25.0, 26.0), "color": (40, 215, 40, 255)},
    {"range": (26.0, 27.0), "color": (50, 205, 50, 255)},
    {"range": (27.0, 28.0), "color": (132, 225, 30, 255)},
    {"range": (28.0, 29.0), "color": (214, 245, 10, 255)},
    {"range": (29.0, 30.0), "color": (255, 255, 0, 255)},
    {"range": (30.0, 31.0), "color": (255, 239, 0, 255)},
    {"range": (31.0, 32.0), "color": (255, 223, 0, 255)},
    {"range": (32.0, 33.0), "color": (255, 215, 0, 255)},
    {"range": (33.0, 34.0), "color": (255, 195, 0, 255)},
    {"range": (34.0, 35.0), "color": (255, 175, 0, 255)},
    {"range": (35.0, 36.0), "color": (255, 165, 0, 255)},
    {"range": (36.0, 37.0), "color": (255, 152, 0, 255)},
    {"range": (37.0, 38.0), "color": (255, 140, 0, 255)},
    {"range": (38.0, 39.0), "color": (255, 104, 0, 255)},
    {"range": (39.0, 40.0), "color": (255, 69, 0, 255)},
    {"range": (40.0, 41.0), "color": (255, 49, 0, 255)},
    {"range": (41.0, 42.0), "color": (255, 29, 0, 255)},
    {"range": (42.0, 43.0), "color": (255, 9, 0, 255)},
    {"range": (43.0, 44.0), "color": (255, 0, 0, 255)},
    {"range": (44.0, 45.0), "color": (208, 0, 0, 255)},
    {"range": (45.0, 46.0), "color": (162, 0, 0, 255)},
    {"range": (46.0, 47.0), "color": (139, 0, 0, 255)},
    {"range": (47.0, 48.0), "color": (134, 0, 0, 255)},
    {"range": (48.0, 49.0), "color": (130, 0, 0, 255)},
    {"range": (49.0, 50.0), "color": (128, 0, 0, 255)},
    {"range": (50.0, 100.0), "color": (128, 0, 0, 255)}  # Maroon
]

base_url = "https://api.openweathermap.org/data/2.5/weather"

for country in countries_list:
    provincias = json.load(open(f"config/{country}.json"))

    image_filler = ImageFiller(f"images/{country}.png", pokemons, temperature_ranges, testing, country)
    success = False

    while not success:
        try:
            image_filler.fill_image()
            success = True
        except Exception as e:
            print(f"Error: {e}")
            sleep(300)

    output_dir = f"images/output/{country}"
    os.makedirs(output_dir, exist_ok=True)

    tomorrow_date = datetime.now() + timedelta(days=1)

    year_month_day = tomorrow_date.strftime("%Y/%m/%d")

    subdirectory = os.path.join(output_dir, year_month_day)
    os.makedirs(subdirectory, exist_ok=True)

    filename = f"{uuid.uuid4()}.webp"

    image_filler.save_image(os.path.join(subdirectory, filename))

exit()
