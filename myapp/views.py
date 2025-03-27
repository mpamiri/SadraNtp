from django.shortcuts import render, redirect
from .forms import NetworkForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Network
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ChangePasswordForm

@login_required(login_url='/login/')
def home_view(request):
    return redirect('status')  

@login_required(login_url='/login/')
def status_view(request):
    network, created = Network.objects.update_or_create(
        id=1,  # فرض کنید همیشه می‌خواید فقط یک نمونه با شناسه ۱ داشته باشید
        defaults={}
    )
    networks = [network]
    return render(request, 'status.html', {'networks': networks} )

@login_required(login_url='/login/')
def information_view(request):
    return render(request, 'information.html')

@login_required(login_url='/login/')
def network_view(request):
    return render(request, 'network.html')

@login_required(login_url='/login/')
def ntp_view(request):
    return render(request, 'ntp.html')

@login_required(login_url='/login/')
def notification_view(request):
    return render(request, 'notification.html')

@login_required(login_url='/login/')
def security_view(request):
    form = ChangePasswordForm()

    if request.method == "POST":
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data["new_password"]
            user = request.user
            user.set_password(new_password)  # Change password
            user.save()
            logout(request)  # Log out the user after password change
            messages.success(request, "Your password has been changed. Please log in again.")
            return redirect("login")  # Redirect to login page

    return render(request, "security.html", {"form": form})

@login_required(login_url='/login/')
def system_view(request):
    return render(request, 'system.html')

@login_required(login_url='/login/')
def network_view(request):
    instance = Network.objects.first()  # Get the existing data if available
    if request.method == "POST":
        form = NetworkForm(request.POST, instance=instance)  # Pre-fill form with existing data
        if form.is_valid():
            form.save()
            return redirect('network')  # Redirect to the same page after saving

    else:
        form = NetworkForm(instance=instance)  # Pre-fill form on page load

    return render(request, "network.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')  