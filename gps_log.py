import serial
import threading
import time

SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

# مقادیر سراسری برای لاگ‌ها
gps_log_data = {
    "time_utc": "N/A",
    "latitude": "N/A",
    "longitude": "N/A",
    "fix_quality": "N/A",
    "satellites": "N/A",
    "hdop": "N/A",
    "altitude": "N/A",
    "geoid_height": "N/A",
    "dgps_update": "N/A",
    "dgps_ref_station_id": "N/A"
}

def parse_lat_long(raw_value, direction):
    if raw_value == "":
        return "N/A"
    degrees = int(float(raw_value) / 100)
    minutes = float(raw_value) - degrees * 100
    decimal_degrees = degrees + minutes / 60
    if direction in ["S", "W"]:
        decimal_degrees = -decimal_degrees
    return round(decimal_degrees, 6)

def gps_log_monitor():
    global gps_log_data
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode('ascii', errors='replace').strip()
                if line.startswith("$GNGGA") or line.startswith("$GPGGA"):
                    parts = line.split(",")
                    if len(parts) >= 15:
                        gps_log_data = {
                            "time_utc": parts[1] or "N/A",
                            "latitude": parse_lat_long(parts[2], parts[3]),
                            "longitude": parse_lat_long(parts[4], parts[5]),
                            "fix_quality": parts[6] or "N/A",              # 0: invalid, 1: GPS fix, 2: DGPS fix
                            "satellites": parts[7] or "N/A",
                            "hdop": parts[8] or "N/A",                      # horizontal dilution of precision
                            "altitude": parts[9] + " " + parts[10] if parts[9] else "N/A",
                            "geoid_height": parts[11] + " " + parts[12] if parts[11] else "N/A",
                            "dgps_update": parts[13] or "N/A",
                            "dgps_ref_station_id": parts[14].split("*")[0] if parts[14] else "N/A"
                        }
                time.sleep(1)
    except Exception as e:
        gps_log_data = {k: "N/A" for k in gps_log_data}

# شروع مانیتور لاگ
log_thread = threading.Thread(target=gps_log_monitor, daemon=True)
log_thread.start()

def get_gps_log_data():
    return gps_log_data
