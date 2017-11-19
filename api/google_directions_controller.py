""" @package google_directions_controller
"""

GOOGLE_API_KEY = ""
GOOGLE_URL = "http://maps.googleapis.com/maps/api/directions/json?"

class DirectionsController:
    """ Esta clase contiene los metodos de comunicacion con la
        API de google, obtencion de direcciones, rutas, etc.
    """

    def __init__(self):
        """Constructor"""

    def get_possible_routes(self, route_request):
        """ Este metodo devuelve las posibles rutas que encontro la API de google
            entre dos pares [latitud, longitud]
            @param route_request los dos puntos del mapa que queremos encontrarle rutas
        """


