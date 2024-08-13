import sys
import os
import requests
from datetime import datetime
from celery import Celery

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.config import db, NVD_API_KEY
from app.models.cve import cve

# Настройка Celery
def make_celery(app_name=__name__):
    redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    celery = Celery(app_name, broker=redis_url)
    celery.conf.update(
        result_backend=redis_url
    )
    return celery

celery_app = make_celery()

@celery_app.task
def fetch_nvd_data(start_year=2020):
    base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    headers = {
        "Api-Key": NVD_API_KEY
    }
    
    current_year = datetime.now().year
    
    for year in range(start_year, current_year + 1):
        pub_start_date = f"{year}-01-01T00:00:00.000Z"
        pub_end_date = f"{year}-12-31T23:59:59.999Z"
        
        params = {
            'pubStartDate': pub_start_date,
            'pubEndDate': pub_end_date,
            'resultsPerPage': 2000  # Максимальное количество результатов на страницу
        }
        
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('vulnerabilities', []):
                cve_data = {
                    "_id": item['cve']['id'],
                    "cve_id": item['cve']['id'],
                    "description": item['cve']['descriptions'][0]['value'],
                    "published_date": item['published'],
                    "last_modified_date": item['lastModified'],
                    "cvss_score": item.get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseScore'),
                    "cvss_vector": item.get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {}).get('vectorString'),
                    "references": [ref['url'] for ref in item['cve']['references']],
                    "vulnerable_configuration": [config['cpe23Uri'] for config in item.get('configurations', {}).get('nodes', [])]
                }

                # Используем upsert для обновления или добавления записи
                db.cves.update_one({'_id': cve_data['_id']}, {'$set': cve_data}, upsert=True)
        else:
            print(f"Failed to fetch data for year {year}: {response.status_code}")

    return "NVD data fetched and stored in MongoDB"
