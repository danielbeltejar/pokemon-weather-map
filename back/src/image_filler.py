import locale
from datetime import timedelta, datetime
from time import sleep

import requests
from PIL import Image, ImageDraw, ImageFont
from ollama import Client

from src.ai_forecast import AIForecast
from src.image_pokemon import ImagePokemon
from src.models import PointOfInterest
from src.weather_translations import WeatherTranslations


class ImageFiller:
    def __init__(self, image_path, pokemons, temperature_ranges, logger, testing, country, provinces):
        self.logger = logger
        self.image = Image.open(image_path).convert("RGBA")
        self.width, self.height = self.image.size
        self.pokemons = pokemons
        self.temperature_ranges = temperature_ranges
        self.testing = testing
        self.country = country
        self.provinces = provinces
        self.weather_conditions = []
        self.poi_list = []

    def fill_image(self):

        for provincia, coords in self.provinces.items():
            sleep(0.1)

            base_url = f"https://v1.wttr.in/{provincia.rstrip()}?format=j1"
            x, y = map(int, coords.split(","))
            seed_point = (x, y)

            data = self._get_weather_data(base_url)

            if data:
                average_temperature = float(data['weather'][1]['avgtempC']) + 3
                weather_condition = self._get_most_common_weather_condition(data['weather'][1]["hourly"])

                associate = self._associate_pokemon(average_temperature, weather_condition)
                pokemon_name, weather_condition = associate

                fill_color = self._determine_fill_color(average_temperature)

                if fill_color:
                    self._log_poi_data(provincia, weather_condition, average_temperature, pokemon_name, fill_color)
                    self.poi_list.append(PointOfInterest(provincia, pokemon_name, average_temperature, x, y, weather_condition))

                    self._bucket_fill(seed_point, fill_color)
                    self._paste_pokemon_image(x, y, pokemon_name)
                    self._add_weather_condition(weather_condition)
                else:
                    self.logger.error(f"No suitable color found for temperature {average_temperature}°C")

        self._add_temperature_labels(self.poi_list)
        self._draw_weather_conditions()
        self._add_legend()
        self._draw_title()
        self.poi_list.clear()

    def _get_weather_data(self, base_url):
        response = requests.get(base_url)
        if response.status_code == 200:
            return response.json()

    def _get_most_common_weather_condition(self, hourly_data):
        weather_desc_count = {}
        for entry in hourly_data:
            weather_desc_value = entry['weatherDesc'][0]['value']
            weather_desc_count[weather_desc_value] = weather_desc_count.get(weather_desc_value, 0) + 1
        return max(weather_desc_count, key=weather_desc_count.get)

    def _determine_fill_color(self, temperature):
        for temp_range in self.temperature_ranges:
            if temp_range["range"][0] <= temperature < temp_range["range"][1]:
                return temp_range["color"]
        return None

    def _log_poi_data(self, provincia, condition, temperature, pokemon, color):
        self.logger.info(
            "Point of Interest data log",
            extra={
                "poi": provincia,
                "weather_condition": condition,
                "average_temperature": f"{temperature}°C",
                "pokemon_name": pokemon,
                "color": color,
            }
        )

    def _paste_pokemon_image(self, x, y, pokemon_name):
        pokemon_image = ImagePokemon(self.image, (x, y), (110, 110), pokemon_name, artwork=True)
        pokemon_image.paste_pokemon_on_filled_image()

    def _add_weather_condition(self, condition):
        translated_weather = WeatherTranslations(country=self.country).translate(condition)
        if translated_weather not in self.weather_conditions:
            self.weather_conditions.append(translated_weather)

    def _add_temperature_labels(self, poi_list):
        font_path = "fonts/PokemonGb-RAeo.ttf"
        font = ImageFont.truetype(font_path, 48)
        text_color, outline_color = (0, 0, 0), (250, 250, 250)
        positions = [(x, y) for x in range(-1, 2) for y in range(-1, 2) if x != 0 or y != 0]

        for poi in poi_list:
            text = f"{int(poi.average_temperature)}º"
            x_temp, y_temp = poi.x + 20, poi.y - 40
            for pos in positions:
                ImageDraw.Draw(self.image).text((x_temp + pos[0], y_temp + pos[1]), text, font=font,
                                                       fill=text_color)
            ImageDraw.Draw(self.image).text((x_temp, y_temp), text, font=font, fill=outline_color)

    def _draw_weather_conditions(self):
        font_path = "fonts/PokemonGb-RAeo.ttf"
        font = ImageFont.truetype(font_path, 48)
        text_color = (0, 0, 0)
        x, y = 110, 1398
        _vertical_count = 0

        weather_translations = WeatherTranslations(country=self.country)
        for condition in self.weather_conditions:
            if _vertical_count >= 3:
                x += 515
                y = 1398
                _vertical_count = 0

            ImageDraw.Draw(self.image).text((x, y), condition, font=font, fill=text_color)
            pokemon_name = self.pokemons.get(weather_translations.get_first_key_by_value(condition))
            pokemon_custom_offset = ImagePokemon(self.image, (x, y), (96, 72), pokemon_name, artwork=False,
                                                 x_offset=-42, y_offset=16)
            pokemon_custom_offset.paste_pokemon_on_filled_image()
            y += 60
            _vertical_count += 1

    def _add_legend(self):
        if len(self.weather_conditions) < 9:
            legend_image = Image.open("images/misc/legend_v2.png").convert("RGBA")
            self.image.paste(legend_image, (1260, 1512), legend_image)

    def _draw_title(self):
        font_path = "fonts/PokemonGb-RAeo.ttf"
        font = ImageFont.truetype(font_path, 64)
        W, H = (1600, 275)
        try:
            locale.setlocale(locale.LC_ALL, {'spain': 'es_ES.UTF-8',
                                             'unitedstates': 'en_US.UTF-8',
                                             'germany': 'de_DE.UTF-8'}.get(self.country, ''))
        except locale.Error as e:
            self.logger.error(f"Error setting locale: {e}")
        self.logger.info(f"Using locale {locale.getlocale(locale.LC_ALL)}")

        date = datetime.now() + timedelta(days=1)
        title_text = f"{WeatherTranslations(country=self.country).get_value_by_key('forecast')} {date.strftime('%B')} {int(date.strftime('%d'))}"
        draw = ImageDraw.Draw(self.image)
        _, _, w, h = draw.textbbox((0, 0), title_text, font=font)
        draw.text(((W - w) / 2, (H - h) / 2), title_text, font=font, fill=(0, 0, 128))

    def _associate_pokemon(self, average_temperature, weather_condition) -> list[str]:
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

    def _bucket_fill(self, seed_point, fill_color):
        target_color = self.image.getpixel(seed_point)

        if target_color == fill_color:
            return

        pixels_to_check = [seed_point]
        processed_pixels = set()

        while pixels_to_check:
            x, y = pixels_to_check.pop()

            if (
                    0 <= x < self.width and
                    0 <= y < self.height and
                    self.image.getpixel((x, y)) == target_color and
                    (x, y) not in processed_pixels
            ):
                self.image.putpixel((x, y), fill_color)
                processed_pixels.add((x, y))

                pixels_to_check.extend(
                    [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
                )

    def save_image(self, file_path):
        self.image.save(file_path, format="WEBP")
        self.logger.info(f"Image saved to {file_path}")

    def generate_ai_forecast(self):
        ai_forecast = AIForecast(self.poi_list, self.logger)
        ai_forecast.prompt(Client(host="http://ollama.server.local:11434"), self.country)
        pass
