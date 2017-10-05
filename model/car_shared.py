""" @package model.car_shared
"""
from flask import jsonify

class PropertyCar:
    """Esta clase contiene la informacion de una propiedad de un auto"""

    def __init__(self):
        """Constructor basico"""
        self.name = ""
        self.value = ""

    @staticmethod
    def new_property(name, value):
        """Constructor de la propiedad del auto
            @param name es el nombre de la propiedad del auto
            @param value es el valor de la propiedad del auto
        """
        property_car = PropertyCar()
        property_car.name = name
        property_car.value = value
        return property_car


class CarShared:
    """Esta clase contiene la informacion de un auto"""

    def __init__(self):
        """Constructor basico"""
        self.id_car = ""
        self._ref = ""
        self.owner = ""
        self.properties = []


    @staticmethod
    def new_car(id_car, owner):
        """ Constructor de un auto
            @param id es el identificador del auto
            @param owner es el dueño de la propiedad del auto
        """
        car = CarShared()
        car.id_car = id_car
        car.owner = owner
        return car

    def add_properties(self, name, value):
        """ Agregar una propiedad del auto
            @param name es el nombre de la propiedad del auto
            @param value es el valor de la propiedad del auto
        """
        property_car = PropertyCar.new_property(name, value)
        self.properties.append(property_car)

    def get_json_new_car(self):
        """ Devuelve la informacion del auto que necesita el sharedServer para crearlo
        """
        return jsonify(
            _ref="",
            id="",
            owner="",
            properties=self.properties
        )
