class PointOfInterest:
    def __init__(self, provincia, pokemon_name, average_temperature, x, y, weather_condition: str = None):
        self.provincia = provincia
        self.pokemon_name = pokemon_name
        self.average_temperature = average_temperature
        self.x = x
        self.y = y
        self.weather_condition = weather_condition
