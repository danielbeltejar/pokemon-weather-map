import json
import locale
import os
from datetime import datetime, timedelta
from time import sleep
from typing import List

import requests
from PIL import Image, ImageFont, ImageDraw

from PokemonImage import PokemonImage
from WeatherTranslations import WeatherTranslations


class PointOfInterest:
    def __init__(self, poi_name, pokemon, average_temperature, x, y):
        self.poi_name = poi_name
        self.pokemon = pokemon
        self.average_temperature = average_temperature
        self.x = x
        self.y = y

poi_list: List[PointOfInterest] = []


class ImageFiller:

    def __init__(self, image_path, pokemons, temperature_ranges, request_data: bool = None):
        self.image = Image.open(image_path)
        self.image = self.image.convert("RGBA")  # Convert to RGBA mode for transparency support
        self.width, self.height = self.image.size
        self.filled_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.filled_image.paste(self.image, (0, 0))
        self.pokemons = pokemons
        self.temperature_ranges = temperature_ranges
        self.weather_conditions = []
        self.request_data = request_data

    def associate_pokemon(self, average_temperature, weather_condition) -> list[str]:
        weather_condition: str = weather_condition.lower()

        if weather_condition.__contains__("rain") or weather_condition.__contains__("drizzle"):
            weather_condition = "rain"
        elif weather_condition.__contains__("snow"):
            weather_condition = "snow"
        elif weather_condition.__contains__("sleet") or weather_condition.__contains__("hail"):
            weather_condition = "hail"
        elif weather_condition.__contains__("thunder"):
            weather_condition = "thunderstorm"

        if average_temperature >= 36.0:
            weather_condition = "hottest"
        elif average_temperature >= 34.0:
            weather_condition = "hotter"
        elif average_temperature >= 32.0:
            weather_condition = "hot"
        elif average_temperature <= 5.0:
            weather_condition = "frozen"

        pokemon = self.pokemons.get(weather_condition)
        return [pokemon.lower(), str(weather_condition.lower())]

    def bucket_fill(self, seed_point, fill_color):
        target_color = self.filled_image.getpixel(seed_point)

        if target_color == fill_color:
            return

        pixels_to_check = [seed_point]
        processed_pixels = set()

        while pixels_to_check:
            x, y = pixels_to_check.pop()

            if (
                    0 <= x < self.width and
                    0 <= y < self.height and
                    self.filled_image.getpixel((x, y)) == target_color and
                    (x, y) not in processed_pixels
            ):
                self.filled_image.putpixel((x, y), fill_color)
                processed_pixels.add((x, y))

                pixels_to_check.extend(
                    [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                )

    def fill_image(self):
        from main import provincias

        for provincia, coords in provincias.items():
            base_url = f"https://wttr.in/{provincia}?format=j1"
            x, y = map(int, coords.split(","))
            seed_point = (x, y)

            data = None
            response = None
            if self.request_data is False:

                response = requests.get(base_url)
                data = response.json()
            else:
                filename = f"{provincia}.json"
                filepath = os.path.join("test/data/", filename)
                if os.path.exists(filepath):
                    with open(filepath, "r") as file:
                        data = json.load(file)

            if self.request_data or response.status_code == 200:
                next_day_weather = data['weather'][1]  # Index 1 corresponds to the next day's weather
                average_temperature = float(next_day_weather['avgtempC'])
                weather_condition = next_day_weather['hourly'][3]['weatherDesc'][0]['value']

                associate = self.associate_pokemon(average_temperature, weather_condition)
                pokemon_name = associate[0]
                weather_condition = associate[1]

                fill_color = None
                for temp_range in self.temperature_ranges:
                    if temp_range["range"][0] <= average_temperature < temp_range["range"][1]:
                        fill_color = temp_range["color"]
                        break

                if fill_color is not None:
                    print(f"POI: {provincia}")
                    print(f"Weather condition: {weather_condition}")
                    print(f"Avg Temp: {average_temperature}°C")
                    print(f"Pokémon: {pokemon_name}")
                    print(f"Color: {fill_color}")

                    poi = PointOfInterest(provincia, pokemon_name, average_temperature, x, y)
                    poi_list.append(poi)

                    self.bucket_fill(seed_point, fill_color)

                    pokemon_image = PokemonImage(self.filled_image, (x, y), (110, 110), pokemon_name, artwork=True)
                    pokemon_image.paste_pokemon_on_filled_image()

                    translated_weather = WeatherTranslations().translate(weather_condition)

                    if not self.weather_conditions.__contains__(translated_weather):
                        self.weather_conditions.append(translated_weather)

                    print()
                else:
                    print(f"No se encontró un color adecuado para la temperatura {average_temperature}°C")
            if self.request_data:
                continue
            sleep(0.05)

        font_path = "fonts/PokemonGb-RAeo.ttf"
        font_size = 48
        font = ImageFont.truetype(font_path, font_size)
        text_color = (0, 0, 0)

        _vertical_count = 0
        x = 110
        y = 1398

        for poi in poi_list:
            ImageDraw.Draw(self.filled_image).text((poi.x + 20, poi.y - 40), str(int(poi.average_temperature)) + "c",
                                                   font=ImageFont.truetype(font_path, 24), fill=(140,140,140))

        for weather_condition in self.weather_conditions:
            if _vertical_count >= 3:
                x += 515
                y = 1398
                _vertical_count = 0

            ImageDraw.Draw(self.filled_image).text((x, y), weather_condition, font=font, fill=text_color)

            weather_translations = WeatherTranslations()

            pokemon_name = self.pokemons.get(weather_translations.get_first_key_by_value(weather_condition))
            pokemon_custom_offset = PokemonImage(self.filled_image, (x, y), (96, 72), pokemon_name, artwork=False,
                                                 x_offset=-42, y_offset=16)
            pokemon_custom_offset.paste_pokemon_on_filled_image()

            y += 60
            _vertical_count += 1

        if len(self.weather_conditions) < 8:
            legend_image = Image.open("images/misc/legend.png")
            legend_image = legend_image.convert("RGBA")
            self.filled_image.paste(legend_image, (1250, 1465), legend_image)

        font = ImageFont.truetype(font_path, 64)
        W, H = (1600, 275)
        locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')

        date = datetime.now() + timedelta(days=1)
        month = date.strftime("%B")
        day = date.strftime("%d")

        title_text = f"Pronóstico {month} {day}"
        text_color = (0, 0, 128)

        draw = ImageDraw.Draw(self.filled_image)
        _, _, w, h = draw.textbbox((0, 0), title_text, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), title_text, font=font, fill=text_color)

    def save_image(self, output_path):
        self.filled_image.convert("RGB").save(output_path, "WEBP", quality=85)
        self.filled_image.show()
