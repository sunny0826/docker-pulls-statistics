import pandas as pd
import json

def convert_csv_to_json():
    df = pd.read_csv('data/stats.csv')
    result = {
        'dates': df['date'].tolist(),
        'kwdb': df['kwdb/kwdb'].tolist(),
        'kwdb_comp_env': df['kwdb/kwdb_comp_env'].tolist(),
        'github_release_downloads': df['kwdb/release'].tolist()
    }
    with open('docs/data/stats.json', 'w') as f:
        json.dump(result, f, indent=2)

if __name__ == '__main__':
    convert_csv_to_json()