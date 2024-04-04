from django.urls import path, include

from rest_framework import routers

from airport.views import (
    AirplaneTypeViewSet,
    AirportViewSet,
    AirplaneViewSet,
    FlightViewSet,
    RouteViewSet,
    OrderViewSet,
    TicketViewSet,
    CityViewSet,
    CrewViewSet
)

router = routers.DefaultRouter()
router.register("airplanetypes", AirplaneTypeViewSet)
router.register("airplane", AirplaneViewSet)
router.register("city", CityViewSet)
router.register("airport", AirportViewSet)
router.register("route", RouteViewSet)
router.register("flight", FlightViewSet)
router.register("ticket", TicketViewSet)
router.register("order", OrderViewSet)
router.register("crew", CrewViewSet)


urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
