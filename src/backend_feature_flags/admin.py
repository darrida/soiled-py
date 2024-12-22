from django.contrib import admin
from django.http import HttpRequest

from backend_feature_flags.models import Feature


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    readonly_fields = ["created_by", "created_at", "updated_by", "updated_at"]

    def save_model(self, request: HttpRequest, obj: Feature, form, change):
        if not obj.created_by:
            obj.created_by = request.user.username
        obj.updated_by = request.user.username
        super().save_model(request, obj, form, change)