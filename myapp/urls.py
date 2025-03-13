from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import home_view , status_view , information_view , network_view , ntp_view , notification_view , security_view, system_view , logout_view  

urlpatterns = [
    path('', home_view, name='home'),
    path('status', status_view, name='status'),
    path('information', information_view, name='information'),
    path('network', network_view, name='network'),
    path('ntp', ntp_view, name='ntp'),
    path('notification', notification_view, name='notification'),
    path('security', security_view, name='security'),
    path('system', system_view, name='system'),
    path('logout', logout_view, name='logout'),
]

