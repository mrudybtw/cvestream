import subprocess
import sys
import os
import time

# Добавление корневого каталога в sys.path для корректного импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def start_celery_worker():
    """Запускает Celery воркер в фоновом режиме"""
    command = [sys.executable, "-m", "celery", "-A", "app.workers.nvd_worker.celery_app", "worker", "--loglevel=info"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print("Error starting Celery worker:", stderr.decode())
    else:
        print("Celery worker output:", stdout.decode())
    return process

def run_db_updater():
    """Запускает db_updater"""
    command = [sys.executable, "app/db_updater.py"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print("Error running db_updater:", stderr.decode())
    else:
        print("db_updater output:", stdout.decode())
    return process

def main():
    # Запуск Celery воркера
    celery_process = start_celery_worker()
    
    # Даем немного времени для старта Celery воркера
    time.sleep(10)  # Можно увеличить время, если нужно

    # Запуск db_updater
    run_db_updater()

    # Завершаем Celery воркер, если db_updater завершился
    celery_process.terminate()
    celery_process.wait()

if __name__ == "__main__":
    main()
