from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse
from .models import Booking
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
    bookings = Booking.objects.all()
    
    if property_id:
        bookings = bookings.filter(property_id=property_id)
        
    events = []
    for booking in bookings:
        color = '#3b82f6' # Blue default
        if booking.status == Booking.Status.CONFIRMED:
            color = '#10b981' # Green
        elif booking.status == Booking.Status.CANCELED:
            color = '#ef4444' # Red
            
        events.append({
            'id': booking.id,
            'title': str(booking.customer), # Or booking.property.name + ' - ' + booking.customer.last_name
            'start': booking.check_in.isoformat(),
            'end': booking.check_out.isoformat(), # FullCalendar end date is exclusive, might need +1 day
            'color': color,
            'url': reverse('customer_detail', args=[booking.customer.id]),
            # 'extendedProps': {'price': booking.total_price}
        })
    return JsonResponse(events, safe=False)
