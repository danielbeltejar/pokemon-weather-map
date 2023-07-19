from PIL import Image


class PokemonImage:
    def __init__(self, image, coords, size, pokemon, artwork=True, x_offset=0, y_offset=0):
        self.filled_image = image
        self.pokemon_image = self._load_pokemon_image(pokemon, artwork, size)
        self.paste_x, self.paste_y = self._calculate_paste_coordinates(coords, x_offset, y_offset)

    def _load_pokemon_image(self, pokemon, artwork, size):
        folder = "artwork" if artwork else "pixel"
        image_path = f"images/pokemon/{folder}/{pokemon}.png"
        pokemon_image = Image.open(image_path).convert("RGBA")
        return pokemon_image.resize(size)

    def _calculate_paste_coordinates(self, coords, x_offset, y_offset):
        pokemon_width, pokemon_height = self.pokemon_image.size
        paste_x = coords[0] - pokemon_width // 2 + x_offset
        paste_y = coords[1] - pokemon_height // 2 + y_offset
        return paste_x, paste_y

    def paste_pokemon_on_filled_image(self):
        self.filled_image.paste(self.pokemon_image, (self.paste_x, self.paste_y), self.pokemon_image)
