import uuid
from datetime import datetime, timedelta
import os
from time import sleep

from dotenv import load_dotenv

from ImageFiller import ImageFiller

load_dotenv()
testing = bool(os.getenv("DEBUG")) if os.getenv("DEBUG") else False

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

provincias = {
    "Asturias": "491,324",
    "Arrecife": "1514,1158",
    "Ceuta": "523,1314",
    "Melilla": "806,1351",
    "Ibiza": "1256,864",
    "Formentera": "1254,924",
    "Mahon, Spain": "1488,735",
    "Gran Canaria": "1449,1281",
    "Tenerife": "1054,1329",
    "San Sebastián de La Gomera": "1152,1270",
    "Santa Cruz de La Palma": "1079,1179",
    "Álava": "826,388",
    "Albacete": "888,934",
    "Alicante": "1025,970",
    "Almería": "859,1142",
    "Ávila": "593,687",
    "Badajoz": "452,943",
    "Barcelona": "1280,541",
    "Burgos": "726,464",
    "Cáceres": "456,794",
    "Cádiz": "477,1227",
    "Cantabria": "673,346",
    "Castellón": "1072,725",
    "Ciudad Real": "703,904",
    "Córdoba": "598,1028",
    "Cuenca": "858,775",
    "Gerona": "1352,477",
    "Granada": "736,1140",
    "Guadalajara": "821,663",
    "Guipúzcoa": "858,347",
    "Huelva": "372,1072",
    "Huesca": "1065,462",
    "Illes Balears": "1395,798",
    "Jaén": "735,1025",
    "La Coruña": "252,330",
    "La Rioja": "834,462",
    "Las Palmas": "1336,1300",
    "León": "506,418",
    "Lérida": "1177,499",
    "Lugo": "350,365",
    "Madrid": "716,695",
    "Málaga": "605,1180",
    "Murcia": "946,1030",
    "Navarra": "913,406",
    "Orense": "333,470",
    "Palencia": "630,444",
    "Pontevedra": "245,424",
    "Salamanca": "472,648",
    "Segovia": "684,609",
    "Sevilla": "494,1097",
    "Soria": "826,546",
    "Tarragona": "1164,608",
    "Santa Cruz de Tenerife": "1225,1247",
    "Teruel": "993,691",
    "Toledo": "657,787",
    "Valencia": "1023,853",
    "Valladolid": "603,560",
    "Bizkaia": "808,333",
    "Zamora": "489,536",
    "Zaragoza": "966,554"
}

base_url = "https://api.openweathermap.org/data/2.5/weather"

image_filler = ImageFiller("images/spain.png", pokemons, temperature_ranges, testing)
success = False

while not success:
    try:
        image_filler.fill_image()
        success = True
    except Exception as e:
        print(f"Error: {e}")
        sleep(300)


output_dir = "images/output/spain"
os.makedirs(output_dir, exist_ok=True)

tomorrow_date = datetime.now() + timedelta(days=1)

year_month_day = tomorrow_date.strftime("%Y/%m/%d")

subdirectory = os.path.join(output_dir, year_month_day)
os.makedirs(subdirectory, exist_ok=True)

filename = f"{uuid.uuid4()}.webp"

image_filler.save_image(os.path.join(subdirectory, filename))

exit()
