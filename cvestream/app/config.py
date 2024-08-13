from pymongo import MongoClient
import os

# Конфигурация подключения к MongoDB
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
MONGO_DB = os.getenv("MONGO_DB", "cve_database")

client = MongoClient(MONGO_HOST, MONGO_PORT)
db = client[MONGO_DB]

# Ключ API для парсинга с NVD
NVD_API_KEY = os.getenv("NVD_API_KEY", "b6ad8680-bbaa-4df3-bc9a-d490e8abd9c9")

# Конфигурация для фильтрации по году
NVD_START_YEAR = int(os.getenv("NVD_START_YEAR", 2020))
