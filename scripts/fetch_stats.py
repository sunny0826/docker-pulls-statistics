import requests
import csv
from datetime import datetime
import os

IMAGES = ['kwdb/kwdb', 'kwdb/kwdb_comp_env']
DATA_PATH = 'data/stats.csv'

def get_docker_stats(image):
    url = f'https://hub.docker.com/v2/repositories/{image}/'
    try:
        response = requests.get(url)
        return response.json()['pull_count']
    except Exception as e:
        print(f'Error fetching {image}: {str(e)}')
        return 0

def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    file_exists = os.path.isfile(DATA_PATH)
    
    with open(DATA_PATH, 'a' if file_exists else 'w', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date'] + IMAGES)
        writer.writerow([datetime.now().strftime('%Y-%m-%d')] + data)

if __name__ == '__main__':
    stats = [get_docker_stats(img) for img in IMAGES]
    save_data(stats)
    print('Data collected successfully:', stats)