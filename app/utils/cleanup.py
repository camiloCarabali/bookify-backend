import os
import time


def cleanup_old_files(directory: str, max_age_minutes: int = 60):
    now = time.time()
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_time = os.path.getmtime(file_path)
            if now - file_time > max_age_minutes * 60:
                os.remove(file_path)


def schedule_cleanup(directory: str, interval_minutes: int = 60):
    while True:
        print(f"[INFO] Limpieza de archivos en {directory}")
        cleanup_old_files(directory)
        time.sleep(interval_minutes * 60)
