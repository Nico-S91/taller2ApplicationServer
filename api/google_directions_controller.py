""" @package google_directions_controller
"""
import requests

GOOGLE_API_KEY = "AIzaSyC0Ro5dttq9RUlR78Lta4_exF8fIK1qgxM"
GOOGLE_URL = "http://maps.googleapis.com/maps/api/directions/json?"

class DirectionsController:
    """ Esta clase contiene los metodos de comunicacion con la
        API de google, obtencion de direcciones, rutas, etc.
    """

    def __init__(self):
        """Constructor"""

    def _get_google_directions(self, parameters):
        """ Get al endpoint de google directions api
            @param parameters los parametros de busqueda para la api
        """
        url = self._get_url(parameters)
        response_google_api = requests.get(url)
        return response_google_api

    def _get_url(self, parameters):
        """ Devuelve la url formada para pegarle a la api de google
            @param clase con parametros para pegarle a la api
        """
        return GOOGLE_URL + "origin=" + str(parameters["origin_lat"]) + "," + str(parameters["origin_long"]) + "&destination=" + str(parameters["destination_lat"]) + "," + str(parameters["destination_long"]) + "&key=" + GOOGLE_API_KEY
