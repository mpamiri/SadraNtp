import serial
import threading
import time

# تنظیمات پورت
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

# مقادیر سراسری
satellite_count = 0
gps_status = "Not Fixed"
latitude = None
longitude = None
fix_quality = 0
hdop = None
altitude = None
geoid_height = None
dgps_update = None
dgps_ref_station_id = None
utc_time = None

last_update_time = time.time()

def gps_satellite_monitor():
    global satellite_count, gps_status, latitude, longitude, fix_quality, hdop
    global altitude, geoid_height, dgps_update, dgps_ref_station_id, utc_time, last_update_time

    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode("ascii", errors="replace").strip()
                if line.startswith("$GNGGA") or line.startswith("$GPGGA"):
                    parts = line.split(",")
                    if len(parts) >= 15:
                        try:
                            utc_time = parts[1] if parts[1] else None
                            lat = parts[2]
                            lat_dir = parts[3]
                            lon = parts[4]
                            lon_dir = parts[5]
                            fix_quality = int(parts[6]) if parts[6].isdigit() else 0
                            satellite_count = int(parts[7]) if parts[7].isdigit() else 0
                            hdop = float(parts[8]) if parts[8] else None
                            altitude = float(parts[9]) if parts[9] else None
                            geoid_height = float(parts[11]) if parts[11] else None
                            dgps_update = parts[13] if parts[13] else None
                            dgps_ref_station_id = parts[14] if parts[14] else None

                            # تبدیل مختصات
                            latitude = convert_to_decimal(lat, lat_dir)
                            longitude = convert_to_decimal(lon, lon_dir)

                            # وضعیت GPS بر اساس تمام داده‌ها
                            if fix_quality > 0 and satellite_count > 0 and latitude is not None and longitude is not None:
                                gps_status = "Fixed"
                            else:
                                gps_status = "Not Fixed"

                            last_update_time = time.time()

                        except ValueError:
                            pass

                # اگر بیشتر از 5 ثانیه داده نیامد، همه چیز ریست شود
                if time.time() - last_update_time > 5:
                    satellite_count = 0
                    gps_status = "Not Fixed"
                    latitude = None
                    longitude = None
                    fix_quality = 0
                    hdop = None
                    altitude = None
                    geoid_height = None
                    dgps_update = None
                    dgps_ref_station_id = None
                    utc_time = None

    except Exception as e:
        gps_status = "Not Fixed"
        satellite_count = 0

# تابع تبدیل مختصات
def convert_to_decimal(value, direction):
    if not value or not direction:
        return None
    try:
        degrees = int(value[:2])
        minutes = float(value[2:])
        decimal = degrees + minutes / 60
        if direction in ['S', 'W']:
            decimal = -decimal
        return decimal
    except:
        return None

# توابع جدا برای هر مقدار
def get_satellite_count(): return satellite_count
def get_gps_status(): return gps_status
def get_latitude(): return latitude
def get_longitude(): return longitude
def get_fix_quality(): return fix_quality
def get_hdop(): return hdop
def get_altitude(): return altitude
def get_geoid_height(): return geoid_height
def get_dgps_update(): return dgps_update
def get_dgps_ref_station_id(): return dgps_ref_station_id
def get_utc_time(): return utc_time

# اجرای نخ پس‌زمینه
sat_thread = threading.Thread(target=gps_satellite_monitor, daemon=True)
sat_thread.start()

# پرینت تست
if __name__ == "__main__":
    while True:
        print("------ GPS LIVE DATA ------")
        print("Time (UTC):", get_utc_time())
        print("Latitude:", get_latitude())
        print("Longitude:", get_longitude())
        print("Fix Quality:", get_fix_quality())
        print("Satellites:", get_satellite_count())
        print("HDOP:", get_hdop())
        print("Altitude:", get_altitude())
        print("Geoid Height:", get_geoid_height())
        print("DGPS Update:", get_dgps_update())
        print("DGPS Ref Station ID:", get_dgps_ref_station_id())
        print("Status:", get_gps_status())
        print("---------------------------\n")
        time.sleep(2)
