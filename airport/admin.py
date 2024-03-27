from django.contrib import admin

from .models import (
    AirplaneType,
    Airport,
    Airplane,
    Route,
    Flight,
    Order,
    Ticket,
    City
)


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInline,)


admin.site.register(AirplaneType)
admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(Flight)
admin.site.register(City)
