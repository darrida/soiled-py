from waffle.apps import WaffleConfig
from social_django.apps import PythonSocialAuthConfig
from django.contrib.auth.apps import AuthConfig

class BackendAuthConfig(AuthConfig):
    verbose_name = "Settings Authentication"

class SvcWaffleConfig(WaffleConfig):
    verbose_name = "Settings Feature Flags"

class BackendSocialAuthConfig(PythonSocialAuthConfig):
    verbose_name = "Settings Social Auth"