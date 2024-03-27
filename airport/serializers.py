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
        fields = ("id", "name", "closest_big_city")


class AirportListSerializer(serializers.ModelSerializer):
    closest_big_city = serializers.SlugRelatedField(
        slug_field="name",
        queryset=City.objects.all()
    )

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirportDetailSerializer(serializers.ModelSerializer):
    closest_big_city = CitySerializer(many=False, read_only=True)

    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.SlugRelatedField(
        slug_field="name",
        queryset=AirplaneType.objects.all()
    )

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class AirplaneDetailSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer(many=False, read_only=True)

    class Meta:
        model = Airplane
        fields = ("id", "name", "rows", "seats_in_row", "airplane_type")


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = "__all__"


class FlightListSerializer(AirplaneSerializer):
    route = serializers.StringRelatedField(many=False, read_only=True)
    airplane = serializers.StringRelatedField(many=False, read_only=True)
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = "__all__"


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.StringRelatedField(source=f"source.name", read_only=True)
    destination = serializers.StringRelatedField(source="destination.name", read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(serializers.ModelSerializer):
    source = AirportSerializer(many=False, read_only=True)
    destination = AirportSerializer(many=False, read_only=True)

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(many=False, read_only=True)
    airplane = AirplaneSerializer(many=False, read_only=False)
    crew = CrewSerializer(many=True, read_only=False)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
