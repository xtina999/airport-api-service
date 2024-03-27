from rest_framework import serializers

from airport.models import (
    AirplaneType,
    Airport,
    Airplane,
    Flight,
    Route,
    Order,
    Ticket,
    City,
    Crew
)


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = "__all__"


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = "__all__"


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = "__all__"


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = "__all__"


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = "__all__"


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
