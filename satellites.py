import serial
import threading
import time

# تنظیمات سریال
SERIAL_PORT = "/dev/ttyAMA0"  # پورت سریال روی Raspberry Pi
BAUD_RATE = 9600            # نرخ باود GPS

# متغیر سراسری برای ذخیره تعداد ماهواره‌ها و زمان آخرین به‌روز‌رسانی
satellite_count = 0
last_update_time = time.time()

def gps_satellite_monitor():
    global satellite_count, last_update_time
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                line = ser.readline().decode('ascii', errors='replace').strip()
                # چک کردن جمله‌های GNGGA یا GPGGA که اطلاعات ماهواره را دارند
                if line.startswith("$GNGGA") or line.startswith("$GPGGA"):
                    parts = line.split(",")
                    if len(parts) > 7:
                        try:
                            count = int(parts[7])
                            satellite_count = count
                            last_update_time = time.time()
                        except ValueError:
                            # اگر تبدیل عددی شکست خورد، مقدار قبلی نگه داشته می‌شود
                            pass
                # اگر بیش از 5 ثانیه داده جدید دریافت نشود، تعداد ماهواره را صفر کن
                if time.time() - last_update_time > 5:
                    satellite_count = 0
    except Exception as e:
        # در صورت بروز خطا (مثلاً قطع شدن GPS یا عدم دسترسی به پورت)
        satellite_count = 0

# راه‌اندازی رشته‌ی پس‌زمینه برای نظارت بر GPS
sat_monitor_thread = threading.Thread(target=gps_satellite_monitor, daemon=True)
sat_monitor_thread.start()

def get_satellite_count():
    return satellite_count

# تست کد در حالت مستقل
if __name__ == "__main__":
    while True:
        print("Satellites Connected:", get_satellite_count())
        time.sleep(1)
