import uuid
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from ImageFiller import ImageFiller

load_dotenv()
testing = bool(os.getenv("DEBUG")) if os.getenv("DEBUG") else False
api_key = os.getenv("API_KEY")

pokemons = {
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
    {"range": (-100.0, 0.0), "color": (135, 206, 250, 255)},  # Light Blue
    {"range": (0.0, 2.5), "color": (163, 200, 225, 255)},  # Sky Blue
    {"range": (2.5, 5.0), "color": (173, 216, 230, 255)},  # Powder Blue
    {"range": (5.0, 7.5), "color": (176, 223, 228, 255)},  # Light Steel Blue
    {"range": (7.5, 10.0), "color": (176, 224, 230, 255)},  # Light Cyan
    {"range": (10.0, 12.5), "color": (199, 234, 234, 255)},  # Aquamarine
    {"range": (12.5, 15.0), "color": (224, 255, 255, 255)},  # Pale Turquoise
    {"range": (15.0, 17.5), "color": (185, 242, 159, 255)},  # Light Green
    {"range": (17.5, 20.0), "color": (144, 238, 144, 255)},  # Lime Green
    {"range": (20.0, 22.5), "color": (0, 255, 0, 255)},  # Lime
    {"range": (22.5, 25.0), "color": (50, 205, 50, 255)},  # Lime Green (Web)
    {"range": (25.0, 27.5), "color": (255, 255, 0, 255)},  # Yellow
    {"range": (27.5, 30.0), "color": (255, 215, 0, 255)},  # Gold
    {"range": (30.0, 32.5), "color": (255, 165, 0, 255)},  # Orange
    {"range": (32.5, 35.0), "color": (255, 140, 0, 255)},  # Dark Orange
    {"range": (35.0, 37.5), "color": (255, 69, 0, 255)},  # Orange Red
    {"range": (37.5, 40.0), "color": (255, 0, 0, 255)},  # Red
    {"range": (40.0, 42.5), "color": (139, 0, 0, 255)},  # Dark Red
    {"range": (42.5, 45.0), "color": (128, 0, 0, 255)},  # Maroon
    {"range": (45.0, 100.0), "color": (128, 0, 0, 255)}  # Maroon
]

provincias = {
    "Ceuta": "523,1314",
    "Melilla": "806,1351",
    "Ibiza": "1256,864",
    "Formentera": "1254,924",
    "Menorca, Illes Balears": "1488,735",
    "Arrecife, Gran Canaria": "1514,1158",
    "Puerto del Rosario, Gran Canaria": "1449,1281",
    "Valverde, Santa Cruz de Tenerife": "1054,1329",
    "San Sebastian de La Gomera, Santa Cruz de Tenerife": "1152,1270",
    "Santa Cruz de La Palma, Santa Cruz de Tenerife": "1079,1179",
    "Álava": "826,388",
    "Albacete": "888,934",
    "Alicante": "1025,970",
    "Almería": "859,1142",
    "Asturias": "491,324",
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

image_filler = ImageFiller("images/spain.png", pokemons, temperature_ranges, api_key, testing)

image_filler.fill_image()

output_dir = "images/output/spain"
os.makedirs(output_dir, exist_ok=True)

tomorrow_date = datetime.now() + timedelta(days=1)

year_month_day = tomorrow_date.strftime("%Y/%m/%d")

subdirectory = os.path.join(output_dir, year_month_day)
os.makedirs(subdirectory, exist_ok=True)

filename = f"{uuid.uuid4()}.jpg"

image_filler.save_image(os.path.join(subdirectory, filename))

exit()
