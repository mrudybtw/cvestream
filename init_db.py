from pymongo import MongoClient

def initialize_database():
    # Подключение к MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    
    # Создание базы данных и коллекций
    db = client['cve_database']  # Имя вашей базы данных
    
    # Проверка и создание коллекции, если её нет
    if 'cves' not in db.list_collection_names():
        db.create_collection('cves')
        print("Коллекция 'cves' создана")
    else:
        print("Коллекция 'cves' уже существует")

    # Можно добавить другие коллекции и настройки при необходимости

if __name__ == "__main__":
    initialize_database()
