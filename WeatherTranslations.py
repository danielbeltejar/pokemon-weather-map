class WeatherTranslations:
    def __init__(self):
        self.translations = {
            "clear sky": "Despejado",
            "clouds": "Nublado",
            "few clouds": "Pocas nubes",
            "scattered clouds": "Pocas nubes",
            "broken clouds": "Pocas nubes",
            "overcast clouds": "Nublado",
            "smoke": "Humo",
            "haze": "Niebla",
            "dust": "Calima",
            "sand": "Calima",
            "ash": "Ceniza",
            "squalls": "Viento",
            "tornado": "Viento",
            "rain": "Lluvia",
            "drizzle": "Lluvia  ",
            "thunderstorm": "Tormenta",
            "snow": "Nieve",
            "mist": "Niebla",
            "fog": "Niebla",
            "hail": "Granizo",
            "charmander": "Calor",
            "charmeleon": "Sofocante",
            "charizard": "Abrasador"
        }

    def translate(self, weather):
        return self.translations.get(weather, "Desconocido")
