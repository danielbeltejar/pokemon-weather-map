# import the module
from typing import Tuple

import python_weather

import asyncio


class WeatherProvider:
    def __init__(self, town, country):
        self.weather_condition = None
        self.average_temperature = None
        self.poi: str = town + ", " + country
        asyncio.run(self.get_weather())

    async def get_weather(self):
        pass
    def results(self) -> [int, str]:
        return [self.average_temperature, self.weather_condition]


if __name__ == '__main__':
    weather = WeatherProvider("Congosto de Valdavia", "ES")
