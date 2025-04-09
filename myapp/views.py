from django.shortcuts import render, redirect
import subprocess
from .forms import NetworkForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from .models import Network
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ChangePasswordForm
from django.http import JsonResponse
from datetime import datetime, timedelta
from gps_log import get_gps_log_data
from network_config import set_dhcp, set_static_ip
from gps_reader import (
    get_utc_time,
    get_satellite_count,
    get_gps_status,
    get_latitude,
    get_longitude,
    get_fix_quality,
    get_hdop,
    get_altitude,
    get_geoid_height,
    get_dgps_update,
    get_dgps_ref_station_id
)

from system_logs import get_system_logs

def system_log_api(request):
    logs = get_system_logs()
    return JsonResponse({"system_logs": logs})

@login_required
def reboot_system(request):
    if request.method == "POST":
        # اجرای دستور sudo reboot
        subprocess.run(['sudo', 'reboot'], check=True)
        return HttpResponse("System is rebooting...", status=200)
    return HttpResponse("Invalid request", status=400)


def gps_log_api(request):
    # ترکیب موقعیت جغرافیایی در یک رشته (اگر هر دو مقدار معتبر باشند)
    lat = get_latitude()
    lon = get_longitude()
    if lat is not None and lon is not None:
        gps_position = f"{lat}, {lon}"
    else:
        gps_position = "Unknown"
        
    data = {
        "time_utc": get_utc_time(),
        "satellites": get_satellite_count(),
        "gps_status": get_gps_status(),
        "gps_position": gps_position,
        "fix_quality": get_fix_quality(),
        "hdop": get_hdop(),
        "altitude": get_altitude(),
        "geoid_height": get_geoid_height(),
        "dgps_update": get_dgps_update(),
        "dgps_ref_station_id": get_dgps_ref_station_id()
    }
    return JsonResponse(data)

def gps_status_api(request):
    satellites = get_satellite_count()
    gps_status = get_gps_status()
    lat = get_latitude()
    lon = get_longitude()
    return JsonResponse({
        "satellites": satellites,
        "gps_status": gps_status,
        "latitude": lat,
        "longitude": lon
    })



@login_required(login_url='/login/')
def get_time(request):
    iran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
    current_time = iran_time.strftime("%Y-%m-%d %H:%M:%S")
    return JsonResponse({"time": current_time})


@login_required(login_url='/login/')
def home_view(request):
    return redirect('status')  

@login_required(login_url='/login/')
def status_view(request):
    network = Network.objects.first()
    
    if not network:
        network = Network.objects.create()  # اگر چیزی نیست، بساز
    
    return render(request, 'status.html', {'networks': [network]})


@login_required(login_url='/login/')
def information_view(request):
    return render(request, 'information.html')


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
    instance = Network.objects.first()
    
    if request.method == "POST":
        form = NetworkForm(request.POST, instance=instance)
        if form.is_valid():
            network = form.save()

            # Ethernet 0
            if network.dhcp_0:
                set_dhcp("Wired connection 1")
            else:
                if network.ipv4_address and network.gateway:
                    set_static_ip("Wired connection 1", network.ipv4_address, network.gateway)

            # Ethernet 1
            if network.dhcp_1:
                set_dhcp("eth1")
            else:
                if network.ipv4_address_1 and network.gateway:
                    set_static_ip("eth1", network.ipv4_address_1, network.gateway)

            return redirect('network')
    else:
        form = NetworkForm(instance=instance)

    return render(request, "network.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')  
