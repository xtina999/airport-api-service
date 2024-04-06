from typing import Type

from django.db.models import Count, F, QuerySet
from rest_framework import viewsets, serializers

from airport.models import (
    AirplaneType,
    Airport,
    Airplane,
    Flight,
    Route,
    Order,
    Ticket,
    Crew,
    City
)
from airport.permissions import IsAdminOrIsAuthenticatedReadOnly
from airport.serializers import (
    CitySerializer,
    AirplaneTypeSerializer,
    AirplaneSerializer,
    AirportSerializer,
    RouteSerializer,
    FlightSerializer,
    TicketSerializer,
    OrderSerializer,
    CrewSerializer,
    AirplaneListSerializer,
    AirplaneDetailSerializer,
    AirportListSerializer,
    AirportDetailSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    FlightListSerializer,
    FlightDetailSerializer
)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("airplane_type")
        return queryset

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        closest_big_city = self.request.query_params.get("closest_big_city")

        if closest_big_city:
            queryset = queryset.filter(closest_big_city=closest_big_city)
        if self.action == "list":
            queryset = queryset.select_related("closest_big_city")
        return queryset

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "list":
            return AirportListSerializer
        if self.action == "retrieve":
            return AirportDetailSerializer
        return AirportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        source_id = self.request.query_params.get("source")
        destination_id = self.request.query_params.get("destination")
        if self.action == "list":
            queryset = (
                queryset
                .select_related("source", "destination")
            )
        if source_id:
            queryset = queryset.filter(source_id=source_id)
        if destination_id:
            queryset = queryset.filter(destination_id=destination_id)

        return queryset

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        airplane = self.request.query_params.get("airplane")

        if airplane:
            queryset = queryset.filter(airplane=airplane)

        if self.action == "list":
            queryset = (
                queryset
                .select_related("route", "airplane")
                .prefetch_related("crew")
                .annotate(
                    tickets_available=F("airplane__rows")
                    * F("airplane__seats_in_row") - Count("tickets"))
            )
        return queryset.order_by("id")

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset.select_related("flight", "order")
        return queryset.filter(order__user=self.request.user)

    def perform_create(self, serializer) -> None:
        order = serializer.validated_data["order"]
        order.user = self.request.user
        order.save()

        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "list":
            queryset = queryset.select_related("user")
        return queryset.filter(user=self.request.user)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)
