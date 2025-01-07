import json
from typing import List
from ollama import Client

from src.models import PointOfInterest


class AIForecast:
    """
    A class to generate weather forecasts using an AI client.
    """

    def __init__(self, aipoidata_list: List[PointOfInterest], logger):
        """
        Initialize the AIForecast object.

        :param aipoidata_list: List of PointOfInterest objects containing weather data.
        :param logger: Logger instance for logging operations.
        """
        self.logger = logger
        self.aipoidata_list = aipoidata_list

    def _build_prompt(self, country: str) -> str:
        """
        Build the prompt to be sent to the AI model.

        :param country: The country for which the weather forecast is being generated.
        :return: The constructed prompt as a string.
        """
        base_prompt = (
            f"Genera un pronóstico para {country} del tiempo para un país en formato de noticiero de TV. "
            "El pronóstico debe ser general, cubriendo las principales regiones del país sin detallar cada provincia individualmente, "
            "puede haber excepciones si crees que puede ser importante. "
            "Describe las condiciones generales y las temperaturas esperadas para cada zona.\n"
        )

        details = "\n".join(
            f"- En la provincia {datapoint.provincia}, se esperan {datapoint.weather_condition} con temperaturas de {datapoint.average_temperature}°C."
            for datapoint in self.aipoidata_list
        )

        language_suffix = {
            "spain": "En español.",
            "unitedstates": "En ingles.",
            "germany": "En aleman.",
            "japan": "En japones.",
        }.get(country.lower(), "En ingles.")

        return (
            f"{base_prompt}{details}\n"
            "El pronóstico debe ser fácil de entender y adecuado para un noticiero de TV. "
            "Texto plano sin formato y sin saltos de linea. Output JSON with only one key 'message'.\n"
            f"{language_suffix}"
        )

    def generate_forecast(self, client: Client, country: str) -> str:
        """
        Generate a weather forecast using the AI client.

        :param client: The AI client to use for generating the forecast.
        :param country: The country for which the forecast is being generated.
        :return: The generated forecast message as a string.
        """
        prompt = self._build_prompt(country)
        self.logger.info("Prompting to AI client", extra={"prompt_content": prompt})

        try:
            response = client.generate(
                model="llama3.2-vision", prompt=prompt, format="json", context=[]
            ).response
            message = json.loads(response)["message"].replace("\n", "")
            self.logger.info("Generated forecast", extra={"forecast_message": message})
            return message
        except (json.JSONDecodeError, KeyError) as e:
            self.logger.error(
                "Failed to parse AI response", extra={"error_detail": str(e)}
            )
            raise ValueError("Invalid response format from AI client") from e