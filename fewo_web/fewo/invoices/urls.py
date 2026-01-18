from django.urls import path
from . import views

urlpatterns = [
    path("", views.invoice_list, name="invoice_list"),
    path("new/", views.invoice_create, name="invoice_create"),
    path(
        "new/<int:customer_id>/",
        views.invoice_create_for_customer,
        name="invoice_create_for_customer",
    ),
    path("<int:pk>/delete/", views.invoice_delete, name="invoice_delete"),
    path("<int:pk>/update/", views.invoice_update, name="invoice_update"),
]
