from datetime import datetime
from time import sleep

import requests
from PIL import Image


class ImageFiller:
    def __init__(self, image_path, pokemons, temperature_ranges, api_key):
        self.image = Image.open(image_path)
        self.image = self.image.convert("RGBA")  # Convert to RGBA mode for transparency support
        self.width, self.height = self.image.size
        self.filled_image = Image.new("RGBA", (self.width, self.height), (0, 0, 0, 0))
        self.filled_image.paste(self.image, (0, 0))
        self.pokemons = pokemons
        self.temperature_ranges = temperature_ranges
        self.api_key = api_key

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

            params = {
                "q": provincia + ",es",
                "appid": self.api_key,
                "units": "metric",
                "dt": int(datetime.now().replace(hour=12, minute=0, second=0).timestamp())
            }

            response = requests.get(base_url, params=params)
            data = response.json()

            if response.status_code == 200:
                estado_tiempo = data["weather"][0]["description"]
                temperatura = data["main"]["temp"]

                if temperatura >= 36.0:
                    pokemon_asociado = "Charizard"
                elif temperatura >= 34.0:
                    pokemon_asociado = "Charmeleon"
                elif temperatura >= 32.0:
                    pokemon_asociado = "Charmander"
                elif temperatura <= 4.0:
                    pokemon_asociado = "Regice"
                else:
                    pokemon_asociado = self.pokemons.get(estado_tiempo, "Castform")
                pokemon_asociado = pokemon_asociado.lower()

                fill_color = None
                for temp_range in self.temperature_ranges:
                    if temp_range["range"][0] <= temperatura < temp_range["range"][1]:
                        fill_color = temp_range["color"]
                        break

                if fill_color is not None:
                    print(f"Provincia: {provincia}")
                    print(f"Estado del tiempo: {estado_tiempo}")
                    print(f"Pokémon asociado: {pokemon_asociado}")
                    print(f"Temperatura: {temperatura}°C")
                    print(f"Color: {fill_color}")
                    self.bucket_fill(seed_point, fill_color)

                    pokemon_image = Image.open(f"images/pokemons/{pokemon_asociado}.png")
                    pokemon_image = pokemon_image.resize((110, 110))

                    pokemon_width, pokemon_height = pokemon_image.size

                    paste_x = seed_point[0] - pokemon_width // 2
                    paste_y = seed_point[1] - pokemon_height // 2

                    self.filled_image.paste(pokemon_image, (paste_x, paste_y), pokemon_image)

                    print()
                else:
                    print(f"No se encontró un color adecuado para la temperatura {temperatura}°C")
            sleep(0.05)

    def save_image(self, output_path):
        self.filled_image.convert("RGB").save(output_path, "JPEG", quality=90)
        self.filled_image.show()
