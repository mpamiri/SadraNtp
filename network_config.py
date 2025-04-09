import subprocess

def set_dhcp(connection_name):
    # فعال‌سازی DHCP برای IPv4
    subprocess.run(["nmcli", "con", "mod", connection_name, "ipv4.method", "auto"])
    # پاک کردن DNS دستی (در صورت وجود)
    subprocess.run(["nmcli", "con", "mod", connection_name, "ipv4.dns", ""])
    # غیر فعال و فعال‌سازی مجدد کانکشن
    subprocess.run(["nmcli", "con", "down", connection_name])
    subprocess.run(["nmcli", "con", "up", connection_name])


def set_static_ip(interface, ip, gateway):
    subprocess.run(["nmcli", "con", "mod", interface, "ipv4.addresses", ip])
    subprocess.run(["nmcli", "con", "mod", interface, "ipv4.gateway", gateway])
    subprocess.run(["nmcli", "con", "mod", interface, "ipv4.method", "manual"])
    subprocess.run(["nmcli", "con", "up", interface])
