from django.contrib import admin

from .models import Location, Measurement, Plant, Sensor


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "active", "updated_at"]
    search_fields = ["name", "description"]
    list_filter = ["active"]


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ["created_at", "plant__name", "moisture_percent"]
    search_fields = ["plant_name"]
    list_filter = ["plant__name"]


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ["name", "location__name", "sensor__name", "active", "updated_at"]
    search_fields = ["name", "description", "location__name", "sensor__name"]
    list_filter = ["location__name", "sensor__name", "active"]


@admin.register(Sensor)
class SensorAdmin(admin.ModelAdmin):
    list_display = ["name", "mac_address", "active", "updated_at"]
    search_fields = ["name", "description", "mac_address"]
    list_filter = ["active"]