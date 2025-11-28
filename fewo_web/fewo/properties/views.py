from django.shortcuts import render, redirect, get_object_or_404
from .models import Property
from .forms import PropertyForm
from django.contrib import messages

from django.contrib.auth.decorators import login_required

@login_required
def property_list(request):
    properties = Property.objects.filter(user=request.user)
    return render(request, "properties/property_list.html", {"properties": properties})

@login_required
def property_create(request):
    # Check if user has reached the limit
    property_count = Property.objects.filter(user=request.user).count()
    has_subscription = hasattr(request.user, 'profile') and request.user.profile.has_subscription
    
    if property_count >= 1 and not has_subscription:
        messages.error(request, "Sie benötigen ein Abo, um mehr als eine Ferienwohnung anzulegen.")
        return redirect("property_list")

    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.user = request.user
            property_obj.save()
            messages.success(request, "Ferienwohnung erfolgreich erstellt.")
            return redirect("property_list")
    else:
        form = PropertyForm()
    return render(request, "properties/property_form.html", {"form": form, "title": "Neue Ferienwohnung"})

@login_required
def property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == "POST":
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Ferienwohnung erfolgreich aktualisiert.")
            return redirect("property_list")
    else:
        form = PropertyForm(instance=property_obj)
    return render(request, "properties/property_form.html", {"form": form, "title": "Ferienwohnung bearbeiten"})

@login_required
def property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, user=request.user)
    if request.method == "POST":
        property_obj.delete()
        messages.success(request, "Ferienwohnung erfolgreich gelöscht.")
        return redirect("property_list")
    return render(request, "properties/property_confirm_delete.html", {"property": property_obj})

from django.http import JsonResponse

@login_required
def get_property_details(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, user=request.user)
    data = {
        "price_per_night": property_obj.price_per_night,
        "default_breakfast_price": property_obj.default_breakfast_price,
        "default_tax_percent": property_obj.default_tax_percent,
    }
    return JsonResponse(data)
