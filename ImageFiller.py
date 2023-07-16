import json
import os
from datetime import datetime
from time import sleep

import requests
from PIL import Image, ImageFont, ImageDraw

from WeatherTranslations import WeatherTranslations


class ImageFiller:
    def __init__(self, image_path, pokemons, temperature_ranges, api_key, request_data: bool = None):
        self.image = Image.open(image_path)
        self.image = self.image.convert("RGBA")  # Convert to RGBA mode for transparency support
        self.width, self.height = self.image.size
        self.filled_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.filled_image.paste(self.image, (0, 0))
        self.pokemons = pokemons
        self.temperature_ranges = temperature_ranges
        self.api_key = api_key
        self.weather_conditions = []
        self.request_data = request_data

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

        base_url = "https://api.openweathermap.org/data/2.5/weather"

        for provincia, coords in provincias.items():
            x, y = map(int, coords.split(","))
            seed_point = (x, y)

            params = {}
            data = None
            response = None
            if self.request_data is None or self.request_data is False:
                params = {
                    "q": provincia + ",es",
                    "appid": self.api_key,
                    "units": "metric",
                    "dt": int(datetime.now().replace(hour=12, minute=0, second=0).timestamp())
                }
                response = requests.get(base_url, params=params)
                data = response.json()
            else:
                filename = f"{provincia}.json"
                filepath = os.path.join("test/data/", filename)
                if os.path.exists(filepath):
                    with open(filepath, "r") as file:
                        data = json.load(file)

            if self.request_data or response.status_code == 200:
                weather_condition = data["weather"][0]["description"]
                temperatura = data["main"]["temp"]

                if temperatura >= 36.0:
                    pokemon_asociado = "Charizard"
                    weather_condition = pokemon_asociado.lower()
                elif temperatura >= 34.0:
                    pokemon_asociado = "Charmeleon"
                    weather_condition = pokemon_asociado.lower()
                elif temperatura >= 32.0:
                    pokemon_asociado = "Charmander"
                    weather_condition = pokemon_asociado.lower()
                elif temperatura <= 4.0:
                    pokemon_asociado = "Regice"
                else:
                    pokemon_asociado = self.pokemons.get(weather_condition, "Castform")
                pokemon_asociado = pokemon_asociado.lower()

                fill_color = None
                for temp_range in self.temperature_ranges:
                    if temp_range["range"][0] <= temperatura < temp_range["range"][1]:
                        fill_color = temp_range["color"]
                        break

                if fill_color is not None:
                    print(f"Provincia: {provincia}")
                    print(f"Estado del tiempo: {weather_condition}")
                    print(f"Pokémon asociado: {pokemon_asociado}")
                    print(f"Temperatura: {temperatura}°C")
                    print(f"Color: {fill_color}")
                    self.bucket_fill(seed_point, fill_color)

                    pokemon_image = Image.open(f"images/pokemon/artwork/{pokemon_asociado}.png")
                    pokemon_image = pokemon_image.resize((110, 110))

                    pokemon_width, pokemon_height = pokemon_image.size

                    paste_x = seed_point[0] - pokemon_width // 2
                    paste_y = seed_point[1] - pokemon_height // 2

                    self.filled_image.paste(pokemon_image, (paste_x, paste_y), pokemon_image)

                    translated_weather = WeatherTranslations().translate(weather_condition)

                    if not self.weather_conditions.__contains__(translated_weather):
                        self.weather_conditions.append(translated_weather)

                    print()
                else:
                    print(f"No se encontró un color adecuado para la temperatura {temperatura}°C")
            if self.request_data:
                continue
            sleep(0.05)

        font_path = "fonts/PokemonGb-RAeo.ttf"
        font_size = 48
        font = ImageFont.truetype(font_path, font_size)
        text_color = (0, 0, 0)

        _vertical_count = 0
        x = 38
        y = 1392
        for weather_condition in self.weather_conditions:
            if _vertical_count >= 3:
                x += 600
                y = 1392
                _vertical_count = 0

            ImageDraw.Draw(self.filled_image).text((x, y), weather_condition, font=font, fill=text_color)
            y += 60
            _vertical_count += 1

        font = ImageFont.truetype(font_path, 56)
        W, H = (1600, 275)
        title_text = "Pronostico julio 18"
        draw = ImageDraw.Draw(self.filled_image)
        _, _, w, h = draw.textbbox((0, 0), title_text, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), title_text, font=font, fill=text_color)

    def save_image(self, output_path):
        self.filled_image.convert("RGB").save(output_path, "JPEG", quality=90)
        self.filled_image.show()
