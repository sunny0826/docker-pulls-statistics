import requests
import csv
from datetime import datetime
import os
import time

IMAGES = ['kwdb/kwdb', 'kwdb/kwdb_comp_env']
DATA_PATH = 'data/stats.csv'

def get_docker_stats(image, max_retries=3, base_delay=1):
    url = f'https://hub.docker.com/v2/repositories/{image}/'
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()['pull_count']
        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 指数退避
                print(f'Error fetching {image} (attempt {attempt + 1}/{max_retries}): {str(e)}. Retrying in {delay}s...')
                time.sleep(delay)
            else:
                print(f'Failed to fetch {image} after {max_retries} attempts: {str(e)}')
                return 0

def get_github_release_stats(repo, max_retries=3, base_delay=1):
    url = f'https://api.github.com/repos/{repo}/releases'
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # 检查HTTP错误状态码
            releases = response.json()
            # 验证返回数据是否为列表
            if not isinstance(releases, list):
                print(f'Unexpected data format for {repo}: expected list, got {type(releases)}')
                return 0
            total_downloads = 0
            for release in releases:
                # 验证release是否为字典
                if not isinstance(release, dict):
                    print(f'Skipping invalid release entry: {release}')
                    continue
                for asset in release.get('assets', []):
                    # 验证asset是否为字典
                    if isinstance(asset, dict):
                        total_downloads += asset.get('download_count', 0)
                    else:
                        print(f'Skipping invalid asset entry: {asset}')
            return total_downloads
        except requests.exceptions.HTTPError as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 指数退避
                print(f'HTTP error fetching {repo} (attempt {attempt + 1}/{max_retries}): {str(e)}. Retrying in {delay}s...')
                time.sleep(delay)
            else:
                print(f'Failed to fetch GitHub releases for {repo} after {max_retries} attempts: {str(e)}')
                return 0
        except Exception as e:
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 指数退避
                print(f'Error fetching GitHub releases for {repo} (attempt {attempt + 1}/{max_retries}): {str(e)}. Retrying in {delay}s...')
                time.sleep(delay)
            else:
                print(f'Failed to fetch GitHub releases for {repo} after {max_retries} attempts: {str(e)}')
                return 0

def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    file_exists = os.path.isfile(DATA_PATH)
    
    with open(DATA_PATH, 'a' if file_exists else 'w', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['date'] + IMAGES + ['github_release_downloads'])
        writer.writerow([datetime.now().strftime('%Y-%m-%d')] + data)

if __name__ == '__main__':
    docker_stats = [get_docker_stats(img) for img in IMAGES]
    github_stats = get_github_release_stats('kwdb/kwdb')
    stats = docker_stats + [github_stats]
    save_data(stats)
    print('Data collected successfully:', stats)