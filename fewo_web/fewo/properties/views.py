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
