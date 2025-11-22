from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from .forms import CustomerForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, "customers/customer_list.html", {"customers": customers})

@login_required
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Kunde erfolgreich erstellt.")
            return redirect("customer_list")
    else:
        form = CustomerForm()
    return render(request, "customers/customer_form.html", {"form": form, "title": "Neuer Kunde"})

@login_required
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Kunde erfolgreich aktualisiert.")
            return redirect("customer_list")
    else:
        form = CustomerForm(instance=customer)
    return render(request, "customers/customer_form.html", {"form": form, "title": "Kunde bearbeiten"})

@login_required
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        messages.success(request, "Kunde erfolgreich gelöscht.")
        return redirect("customer_list")
    return render(request, "customers/customer_confirm_delete.html", {"customer": customer})
