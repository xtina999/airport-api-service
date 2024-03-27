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
