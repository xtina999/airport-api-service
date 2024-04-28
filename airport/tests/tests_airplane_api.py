from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import AirplaneType, Airplane, Airport, City
from airport.serializers import (
    AirplaneListSerializer,
    AirportListSerializer,
    AirportDetailSerializer
)

AIRPLANE_URL = reverse("airport:airplane-list")
AIRPORT_URL = reverse("airport:airport-list")


def detail_url(airport_id):
    return reverse("airport:airport-detail", args=(airport_id,))


def sample_city(**params):
    defaults = {
        "name": "City"
    }
    defaults.update(params)
    return City.objects.create(**defaults)


def sample_airport(**params):
    defaults = {
        "name": "Type1",
        "closest_big_city": sample_city(),
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {
        "name": "Type1"
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    defaults = {
        "name": "Airplane Name",
        "rows": 5,
        "seats_in_row": 5,
        "airplane_type": sample_airplane_type(),
    }
    defaults.update(params)

    return Airplane.objects.create(**defaults)


class UnauthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(AIRPLANE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_airplanes(self):
        sample_airplane()
        sample_airplane()

        res = self.client.get(AIRPLANE_URL)

        airplane = Airplane.objects.all()
        serializer = AirplaneListSerializer(airplane, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_list_airport(self):
        sample_airport()
        sample_airport()

        res = self.client.get(AIRPORT_URL)
        airport = Airport.objects.all()
        serializer = AirportListSerializer(airport, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_airports_by_city(self):
        airport_1 = sample_airport()
        airport_2 = sample_airport()
        city_1 = City.objects.create(name="Kyiv")
        city_2 = City.objects.create(name="Lviv")

        airport_1.closest_big_city = city_1
        airport_1.save()
        airport_2.closest_big_city = city_2
        airport_2.save()

        res = self.client.get(
            AIRPORT_URL,
            {"closest_big_city": f"{city_1.id}"}
        )

        serializer_with_city_1 = AirportListSerializer(airport_1)
        serializer_with_city_2 = AirportListSerializer(airport_2)

        self.assertIn(serializer_with_city_1.data, res.data["results"])
        self.assertNotIn(serializer_with_city_2.data, res.data["results"])

    def test_retrieve_airport(self):
        airport = sample_airport()

        url = detail_url(airport.id)

        res = self.client.get(url)

        serializer = AirportDetailSerializer(airport)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_airport_forbidden(self):
        payload = {
            "name": "Type1",
            "closest_big_city": sample_city(),
        }

        res = self.client.post(AIRPORT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminAirportTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_admin_airport_create(self):
        city_1 = City.objects.create(name="Kyiv")

        payload = {
            "name": "Type1",
            "closest_big_city": city_1.id,
        }

        res = self.client.post(AIRPORT_URL, payload)

        airport = Airport.objects.get(id=res.data["id"])
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        self.assertEqual(
            payload["closest_big_city"],
            airport.closest_big_city.id
        )
