import json


class WeatherTranslations:
    def __init__(self, country: str):
        self.translations = json.load(open(f"lang/{country}.json", "r"))

    def translate(self, weather):
        return self.translations.get(weather, "Desconocido")

    def get_first_key_by_value(self, value):
        for key, val in self.translations.items():
            if val == value:
                return key
        return None
