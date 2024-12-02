import json

from ollama import Client
from typing import List

from src.models import PointOfInterest


class AIForecast:
    def __init__(self, aipoidata_list: List[PointOfInterest], logger):
        self.logger = logger
        self.aipoidata_list = aipoidata_list

    def prompt(self, client: Client, country: str):
        prompt = (
            f"Genera un pronóstico para {country} del tiempo para un país en formato de noticiero de TV. "
            "El pronóstico debe ser general, cubriendo las principales regiones del país sin detallar cada provincia individualmente, "
            "puede haber excepciones si crees que puede ser importante. "
            "Describe las condiciones generales y las temperaturas esperadas para cada zona.\n"
        )

        for datapoint in self.aipoidata_list:
            prompt += f"- En la provincia {datapoint.provincia}, se esperan {datapoint.weather_condition} con temperaturas de {datapoint.average_temperature}°C.\n"

        prompt += (
            "\nEl pronóstico debe ser fácil de entender y adecuado para un noticiero de TV. "
            "Texto plano sin formato y sin saltos de linea. Output JSON with only one key 'message'."
        )
        if country == "spain":
            prompt += "In spanish."
        elif country == "unitedstates":
            prompt += "In english."
        elif country == "germany":
            prompt += "In german."
        elif country == "japan":
            prompt += "In japanish."

        self.logger.info("Prompting to llama",
                     extra={
                         "prompt": prompt
                     })
        response = client.generate(model="llama3.2-vision", prompt=prompt, format="json", context=[]).response

        self.logger.info(json.loads(response)["message"].replace("\n", ""))
