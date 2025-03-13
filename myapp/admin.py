from django.contrib import admin
from .models import Network

@admin.register(Network)
class NetworkSettingsAdmin(admin.ModelAdmin):
    list_display = ('host_name', 'server_1', 'server_2', 'domain_name', 'ipv4_address', 'gateway', 'dhcp_0', 'ipv4_address_1', 'dhcp_1', 'ntp_server', 'authentication_key')
    search_fields = ('host_name', 'server_1', 'server_2', 'domain_name')
    list_filter = ('dhcp_0', 'dhcp_1')
