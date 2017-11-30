""" @package test.response_mock
"""
class ResponseMock:
    """Esta clase esta para mockear las respuestas del SharedServer"""

    def __init__(self):
        self.data = ""
        self.status_code = 0
        self.text = ""

    def set_response(self, response):
        """Agrega el mensaje al response
            @param response es el mensaje"""
        self.data = response
        self.text = str(response)

    def set_code(self, code):
        """Agrega el codigo al response
            @param code es el codigo de la respuesta"""
        self.status_code = code
