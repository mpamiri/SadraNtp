from django.db import models

class Network(models.Model):
    host_name = models.CharField(max_length=100 , null=True , blank=True)
    server_1 = models.CharField(max_length=100 , null=True , blank=True)
    server_2 = models.CharField(max_length=100 , null=True , blank=True)
    domain_name = models.CharField(max_length=100 , null=True , blank=True)
    
    ipv4_address = models.CharField(max_length=100 , null=True , blank=True)
    gateway = models.CharField(max_length=100 , null=True , blank=True)
    dhcp_0 = models.BooleanField(default=False)

    ipv4_address_1 = models.CharField(max_length=100 , null=True , blank=True)
    dhcp_1 = models.BooleanField(default=False)

    ntp_server = models.CharField(max_length=100 , null=True , blank=True)
    authentication_key = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        Network.objects.all().delete()  # Delete old data
        super(Network, self).save(*args, **kwargs)  # Save new data

    def __str__(self):
        return self.host_name if self.host_name else "Network Settings"