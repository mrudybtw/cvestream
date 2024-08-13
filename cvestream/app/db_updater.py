from app.workers.nvd_worker import fetch_nvd_data

def main():
    # Запуск задачи Celery
    fetch_nvd_data.apply_async(args=[2020])  # Можно изменить год на нужный

if __name__ == "__main__":
    main()
