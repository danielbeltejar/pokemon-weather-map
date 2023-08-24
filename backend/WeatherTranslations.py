class WeatherTranslations:
    def __init__(self):
        self.translations = {
            "hot": "Calor",
            "hotter": "Sofocante",
            "hottest": "Abrasador",
            "frozen": "Helado",
            "rain": "Lluvia",
            "drizzle": "Lluvia",
            "hail": "Granizo",
            "snow": "Nieve",
            "thunderstorm": "Tormenta",
            "clear": "Despejado",
            "sunny": "Despejado",
            "cloudy": "Nublado",
            "partly cloudy": "Nubes",
            "overcast": "Nublado",
            "mist": "Niebla",
            "fog": "Niebla",
            "freezing fog": "Niebla",
            "patchy rain nearby": "Lluvia",
            "patchy rain possible": "Lluvia",
            "patchy light drizzle": "Lluvia",
            "light rain shower": "Lluvia",
            "moderate rain at times": "Lluvia",
            "heavy rain at times": "Lluvia",
            "moderate or heavy rain shower": "Lluvia",
            "patchy light snow": "Nieve",
            "light snow": "Nieve",
            "light snow showers": "Nieve",
            "patchy heavy snow": "Nieve",
            "moderate or heavy snow showers": "Nieve",
            "moderate or heavy snow in area with thunder": "Nieve",
            "patchy snow nearby": "Nieve",
            "light sleet showers": "Nieve",
            "moderate or heavy sleet showers": "Nieve",
            "light showers of ice pellets": "Granizo",
            "thundery outbreaks in nearby": "Tormenta",
            "patchy light rain in area with thunder": "Tormenta",
            "patchy light snow in area with thunder": "Tormenta",
            "light rain": "Lluvia",
            "light drizzle": "Lluvia",
            "patchy light rain": "Lluvia",
            "moderate rain": "Lluvia",
            "heavy rain": "Lluvia",
            "torrential rain shower": "Lluvia",
            "blowing snow": "Nieve",
            "moderate or heavy sleet": "Nieve",
            "blizzard": "Nieve",
            "patchy moderate snow": "Nieve",
            "moderate snow": "Nieve",
            "heavy snow": "Nieve",
            "patchy sleet nearby": "Nieve",
            "patchy freezing drizzle nearby": "Lluvia",
            "freezing drizzle": "Nieve",
            "heavy freezing drizzle": "Nieve",
            "light freezing rain": "Nieve",
            "moderate or heavy freezing rain": "Nieve",
            "light sleet": "Nieve",
            "ice pellets": "Granizo",
            "moderate or heavy showers of ice pellets": "Granizo",
            "moderate or heavy rain in area with thunder": "Granizo"
        }

    def translate(self, weather):
        return self.translations.get(weather, "Desconocido")

    def get_first_key_by_value(self, value):
        for key, val in self.translations.items():
            if val == value:
                return key
        return None
