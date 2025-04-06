import sys
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
pipeline_id = "1"
count = 0

def out_workday(date):
    date_formated = datetime.fromisoformat(date.replace('Z', '+00:00'))
    if date_formated.weekday() == 1:
        return True
    return False
def get_deployments(tk, url):
    global count
    global pipeline_id
    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth('', tk)
        )
        if response.status_code == 200:
            for run in response.json().get('value', []):
                if run['state'] == 'completed' and run['result'] == 'succeeded' and out_workday(run['finishedDate']):
                    count+=1
            badge =f"[![CDNJS](https://img.shields.io/badge/deployments_on_friday-{count}-blue)](https://dev.azure.com/mestevez0043/mestevez/_git/demo-task01?path=/scripts/count_de.py)"
            print(badge)
        else:
            print(f"Request failed with status code {response.status_code}")
            print("Response:", response)   
    except requests.exceptions.RequestException as e:   
        print(f"An error occurred: {e}")
if sys.argv[1:][0] and sys.argv[1:][1] and sys.argv[1:][2]:
    global tk
    global organization
    global project
    tk=sys.argv[1:][0]
    organization=sys.argv[1:][1]
    project=sys.argv[1:][2]
    url = f"https://dev.azure.com/{organization}/{project}/_apis/pipelines/{pipeline_id}/runs?api-version=7.2-preview.1"
    get_deployments(tk,url)

