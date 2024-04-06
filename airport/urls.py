from django.conf import settings
from django.conf.urls.static import static
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

app_name = "airport"
