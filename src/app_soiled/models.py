from django.db import models

null_blank = {
    "on_delete": models.SET_NULL,
    "blank": True,
    "null": True
}

delete_relation = {
    "on_delete": models.SET_NULL,
}

class Sensor(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True, unique=True)
    mac_address = models.CharField(max_length=17, unique=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "Sensor"
        verbose_name_plural = "Sensors"

    def __str__(self):
        return self.name if self.name else self.mac_address
    

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return self.name


class Plant(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True, blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30, null=True, blank=True)

    location = models.ForeignKey("app_soiled.Location", **null_blank)
    sensor = models.ForeignKey("app_soiled.Sensor", **null_blank)

    class Meta:
        verbose_name = "Plant"
        verbose_name_plural = "Plants"

    def __str__(self):
        return self.name
    

class Measurement(models.Model):
    moisture_percent = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=30, null=True, blank=True)

    plant = models.ForeignKey("app_soiled.Plant", models.DO_NOTHING)

    class Meta:
        verbose_name = "Measurement"
        verbose_name_plural = "Measurements"
        get_latest_by = "created_at"

    def __str__(self):
        return f"{self.created_at}"