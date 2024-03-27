from django.db import models


class City(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "cities"
        ordering = ("name",)

    def __str__(self):
        return self.name


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

        def __str__(self):
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

    def __str__(self):
        return f"{self.name}({self.closest_big_city})"


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(
        "AirplaneType",
        on_delete=models.CASCADE,
        related_name="airplanes"
    )

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name
