from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserProfileForm
from .models import UserProfile

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

@login_required
def profile_settings(request):
    # Get or create the user's profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Einstellungen erfolgreich gespeichert.')
            return redirect('profile_settings')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'accounts/profile_settings.html', {'form': form})

@login_required
def subscription_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.has_subscription = True
        profile.save()
        messages.success(request, 'Herzlichen Glückwunsch! Sie haben das Abo erfolgreich abgeschlossen.')
        return redirect('property_list')
        
    return render(request, 'accounts/subscription.html')

@login_required
def cancel_subscription(request):
    if request.method == 'POST':
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.has_subscription = False
        profile.save()
        messages.success(request, 'Ihr Abo wurde erfolgreich gekündigt.')
    return redirect('profile_settings')
