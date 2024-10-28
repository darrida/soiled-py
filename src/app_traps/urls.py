from django.urls import path

from . import views

urlpatterns = [
    # path("", temp, name="temp"),
    path("hx-status-widgets", views.get_traps_status, name="hx_traps_widgets"),
]
