from django.urls import path

from . import views

urlpatterns = [
    path("", views.temp, name="temp"),
    path("hx-status-widgets", views.get_statuses, name="hx_plants_widgets"),
    path("hx-status-table", views.get_status_table, name="hx_plants_table"),
    # path("hx-plant-graph", views.get_plant_graph, name="hx_plant_graph"),
]
