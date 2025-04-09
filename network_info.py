import subprocess

def get_ip_address():
    try:
        # اجرای دستور nmcli برای گرفتن IP آدرس
        output = subprocess.check_output(
            ["nmcli", "-g", "IP4.ADDRESS", "con", "show", "Wired connection 1"],
            universal_newlines=True
        ).strip()
        
        if output:
            print("Wired connection 1 IP Address:", output)
        else:
            print("IP Address not found for Wired connection 1")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

get_ip_address()
