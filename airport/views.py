from rest_framework import viewsets

from airport.models import (
    AirplaneType,
    Airport,
    Airplane,
    Flight,
    Route,
    Order,
    Ticket,
    City,

)


class CityViewSet(viewsets.ModelViewSet):
    queryset = City.objects.all()


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all()


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
