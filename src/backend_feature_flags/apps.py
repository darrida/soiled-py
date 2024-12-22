from django.apps import AppConfig


class BackendFeatureFlagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend_feature_flags'
    verbose_name = "Feature Management"
