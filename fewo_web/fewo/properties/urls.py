from django.urls import path
from . import views

urlpatterns = [
    path("", views.property_list, name="property_list"),
    path("create/", views.property_create, name="property_create"),
    path("<int:pk>/update/", views.property_update, name="property_update"),
    path("<int:pk>/delete/", views.property_delete, name="property_delete"),
    path("<int:pk>/details/", views.get_property_details, name="property_details"),
]
