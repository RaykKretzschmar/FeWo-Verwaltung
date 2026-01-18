from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from invoices.models import Invoice
from properties.models import Property

@login_required
def calendar_view(request):
    property_id = request.GET.get('property')
    context = {}
    if property_id:
        property_obj = get_object_or_404(Property, pk=property_id, user=request.user)
        context['property'] = property_obj
    return render(request, 'bookings/calendar.html', context)

@login_required
def booking_api(request):
    property_id = request.GET.get('property')
    # Filter for invoices that have dates set and belong to the current user
    invoices = Invoice.objects.filter(
        user=request.user,
        arrival_date__isnull=False,
        departure_date__isnull=False
    )
    
    if property_id:
        invoices = invoices.filter(rental_property_id=property_id)
        
    events = []
    for invoice in invoices:
        # Default color for visits
        color = '#3b82f6' 

        customer = invoice.customer
        title = str(customer)
        customer_url = reverse('customer_detail', args=[customer.id])

        events.append({
            'id': invoice.id,
            'title': title,
            'start': invoice.arrival_date.isoformat(),
            'end': invoice.departure_date.isoformat(), 
            'color': color,
            'url': customer_url,
        })
    return JsonResponse(events, safe=False)
