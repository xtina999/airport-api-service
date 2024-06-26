import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from rest_framework.exceptions import ValidationError


class City(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "cities"
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="airports"
    )

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return f"{self.name}({self.closest_big_city})"


def airplane_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)

    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads", "airplanes", filename)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType",
        on_delete=models.CASCADE,
        related_name="airplanes"
    )
    image = models.ImageField(null=True, upload_to=airplane_image_file_path)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_source"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_destination"
    )
    distance = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.source} - {self.destination}({self.destination})"


class Crew(models.Model):
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.position} - {self.name}"


class Flight(models.Model):
    route = models.ForeignKey(
        "Route",
        on_delete=models.CASCADE
    )
    airplane = models.ForeignKey(
        "Airplane",
        on_delete=models.CASCADE,
        related_name="flights"
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    crew = models.ManyToManyField(
        Crew,
        related_name="crews",
        null=True
    )

    def __str__(self) -> str:
        return f"{self.route} - {self.airplane}" \
               f"({self.departure_time}-{self.arrival_time})"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return str(self.created_at)


class Ticket(models.Model):
    passenger = models.CharField(max_length=255, default=None)
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    row = models.IntegerField()
    seat = models.IntegerField()

    def clean(self):
        if self.row is not None and self.seat is not None:
            if not (1 <= self.row <= self.flight.airplane.rows and
                    1 <= self.seat <= self.flight.airplane.seats_in_row):
                raise ValidationError(
                    "Selected seat is not within available range."
                )

        if self.row is not None and self.seat is not None:
            if Ticket.objects.filter(
                    flight=self.flight,
                    row=self.row,
                    seat=self.seat
            ).exclude(pk=self.pk).exists():
                raise ValidationError("Selected seat is already taken.")

    class Meta:
        unique_together = ("seat", "row")
        ordering = ("seat",)

    def __str__(self) -> str:
        return f"{self.flight}(row:{self.row}, seat:{self.seat})"
