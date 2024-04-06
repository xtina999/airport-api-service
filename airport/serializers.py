from django.db import transaction
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


class TicketSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
    route = serializers.StringRelatedField(source="flight.route", read_only=True)
    airplane = serializers.StringRelatedField(source="flight.airplane", read_only=True)
    departure_time = serializers.StringRelatedField(source="flight.departure_time", read_only=True)
    arrival_time = serializers.StringRelatedField(source="flight.arrival_time", read_only=True)
    user = serializers.StringRelatedField(source="order.user", read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "passenger",
            "row",
            "seat",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "order",
            "user"
        )

    def get_user(self, obj):
        return obj.order.user.name if obj.order else None

    def validate(self, data):
        row = data.get('row')
        seat = data.get('seat')
        flight = data.get('flight')

        if not (1 <= row <= flight.airplane.rows and 1 <= seat <= flight.airplane.seats_in_row):
            raise serializers.ValidationError("Selected seat is not within the available range.")

        return data

    def validate_seat(self, value):
        flight = self.context["request"].data.get("flight")

        if flight and Ticket.objects.filter(flight=flight, seat=value).exists():
            raise serializers.ValidationError("Selected seat is already taken.")

        return value


class FlightListSerializer(AirplaneSerializer):
    route = serializers.StringRelatedField(many=False, read_only=True)
    airplane = serializers.StringRelatedField(many=False, read_only=True)
    crew = CrewSerializer(many=True, read_only=True)
    taken_seats = serializers.SerializerMethodField()
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time", "crew", "taken_seats", "tickets_available")

    def get_taken_seats(self, obj):
        return [f"row:{ticket.row} seat:{ticket.seat}" for ticket in obj.tickets.all()]


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
    tickets = TicketSerializer(
        many=True,
        read_only=False,
        allow_empty=False
    )

    class Meta:
        model = Order
        fields = "__all__"

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class TicketListSerializer(TicketSerializer):
    route = serializers.StringRelatedField(source="flight.route", read_only=True)
    airplane = serializers.StringRelatedField(source="flight.airplane", read_only=True)
    departure_time = serializers.StringRelatedField(source="flight.departure_time", read_only=True)
    arrival_time = serializers.StringRelatedField(source="flight.arrival_time", read_only=True)
    order = OrderSerializer(many=False, read_only=True)

    class Meta:
        model = Ticket
        fields = (
            "id",
            "row",
            "seat",
            "route",
            "airplane",
            "departure_time",
            "arrival_time",
            "order"
        )


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(
        many=True,
        read_only=True
    )
