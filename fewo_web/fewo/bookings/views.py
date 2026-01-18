from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from invoices.models import Invoice
from properties.models import Property

def calendar_view(request):
    property_id = request.GET.get('property')
    context = {}
    if property_id:
        property_obj = get_object_or_404(Property, pk=property_id)
        context['property'] = property_obj
    return render(request, 'bookings/calendar.html', context)

def booking_api(request):
    property_id = request.GET.get('property')
    # Filter for invoices that have dates set (though model fields are required)
    invoices = Invoice.objects.filter(arrival_date__isnull=False, departure_date__isnull=False)
    
    if property_id:
        invoices = invoices.filter(rental_property_id=property_id)
        
    events = []
    for invoice in invoices:
        # Default color for visits
        color = '#3b82f6' 
        
        events.append({
            'id': invoice.id,
            'title': str(invoice.customer), 
            'start': invoice.arrival_date.isoformat(),
            'end': invoice.departure_date.isoformat(), 
            'color': color,
            'url': reverse('customer_detail', args=[invoice.customer.id]),
        })
    return JsonResponse(events, safe=False)
