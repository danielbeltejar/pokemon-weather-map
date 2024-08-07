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

    def __init__(self, image_path, pokemons, temperature_ranges, request_data: bool = None, country: str = None):
        self.image = Image.open(image_path)
        self.image = self.image.convert("RGBA")  # Convert to RGBA mode for transparency support
        self.width, self.height = self.image.size
        self.filled_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.filled_image.paste(self.image, (0, 0))
        self.pokemons = pokemons
        self.temperature_ranges = temperature_ranges
        self.weather_conditions = []
        self.request_data = request_data
        self.country = country

    def associate_pokemon(self, average_temperature, weather_condition) -> list[str]:
        weather_condition: str = weather_condition.lower().strip()

        if weather_condition.__contains__("rain") or weather_condition.__contains__("drizzle"):
            weather_condition = "rain"
        elif weather_condition.__contains__("snow"):
            weather_condition = "snow"
        elif weather_condition.__contains__("sleet") or weather_condition.__contains__("hail"):
            weather_condition = "hail"
        elif weather_condition.__contains__("thunder"):
            weather_condition = "thunderstorm"

        if average_temperature >= 34.0:
            weather_condition = "hottest"
        elif average_temperature >= 32.0:
            weather_condition = "hotter"
        elif average_temperature >= 30.0:
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
            base_url = f"https://v1.wttr.in/{provincia.rstrip()}?format=j1"
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
                average_temperature = float(next_day_weather['avgtempC']) + 3

                weather_desc_count = {}

                for entry in next_day_weather["hourly"]:
                    weather_desc_value = entry['weatherDesc'][0]['value']
                    if weather_desc_value in weather_desc_count:
                        weather_desc_count[weather_desc_value] += 1
                    else:
                        weather_desc_count[weather_desc_value] = 1

                weather_condition = max(weather_desc_count, key=weather_desc_count.get)

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

                    translated_weather = WeatherTranslations(country=self.country).translate(weather_condition)

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
        outline_color = (250, 250, 250)
        _vertical_count = 0
        x = 110
        y = 1398

        positions = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]

        for poi in poi_list:
            text = str(int(poi.average_temperature)) + "º"
            x_temp, y_temp = poi.x + 20, poi.y - 40

            # Draw the outline text
            for pos in positions:
                ImageDraw.Draw(self.filled_image).text((x_temp + pos[0], y_temp + pos[1]), text, font=font,
                                                       fill=text_color)

            # Draw the main text
            ImageDraw.Draw(self.filled_image).text((x_temp, y_temp), text, font=font, fill=outline_color)

        poi_list.clear()

        # Draw weather condition text without outline
        _vertical_count = 0
        x = 110
        y = 1398

        weather_translations = WeatherTranslations(country=self.country)

        for weather_condition in self.weather_conditions:
            if _vertical_count >= 3:
                x += 515
                y = 1398
                _vertical_count = 0

            ImageDraw.Draw(self.filled_image).text((x, y), weather_condition, font=font, fill=text_color)

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
        try:
            if self.country == "spain":
                locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
            elif self.country == "unitedstates":
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
            elif self.country == "germany":
                locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8')
        except locale.Error as e:
            print(f"Error setting locale: {e}")

        date = datetime.now() + timedelta(days=1)
        month = date.strftime("%B")
        day = date.strftime("%d")

        title_text = f"{weather_translations.get_value_by_key('forecast')} {month} {str(int(day))}"
        text_color = (0, 0, 128)

        draw = ImageDraw.Draw(self.filled_image)
        _, _, w, h = draw.textbbox((0, 0), title_text, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), title_text, font=font, fill=text_color)

    def save_image(self, output_path, debug: bool):
        self.filled_image = self.filled_image.resize((1080, 1080), resample=Image.BILINEAR)
        self.filled_image.convert("RGB").save(output_path, "WEBP", quality=80)
        if debug:
            self.filled_image.show()
