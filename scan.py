import requests
from time import sleep
from sys import argv
from helpers.redirect import get_redirect_url
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def start_spider(url):
    payload = {"url": get_redirect_url(url)}
    api_url = f"{zap}/api/v1/spider/start"
    r = requests.post(api_url, json=payload)
    return r.json()

def status_spider(scan_id):
    payload = {"scan_id": scan_id}
    api_url = f"{zap}/api/v1/spider/status"
    r = requests.post(api_url, json=payload)
    status_integer = int(r.json()['status'])
    return status_integer

def results_spider(scan_id):
    payload = {"scan_id": scan_id}
    api_url = f"{zap}/api/v1/spider/results"
    r = requests.post(api_url, json=payload)
    return r.json()

def start_ascan(url):
    payload = {"url": url}
    api_url = f"{zap}/api/v1/active/scan"
    r = requests.post(api_url, json=payload)
    return r.json()

def status_ascan(scan_id):
    payload = {"scan_id": scan_id}
    api_url = f"{zap}/api/v1/active/status"
    r = requests.post(api_url, json=payload)
    return r.json()

def get_results(url):
    payload = {"url": url}
    api_url = f"{zap}/api/v1/results/summary"
    r = requests.post(api_url, json=payload)
    return r.json()


def main(url):
    scan_id = start_spider(url)['scan_id']
    progress = status_spider(scan_id)

    while progress < 90:
        print(f"Spider Progress: {progress}")
        progress = status_spider(scan_id)
        sleep(2)
    
    results = results_spider(scan_id)
    print(f"\n\n SPIDER RESULTS \n\n")
    for i in results:
        print(i)

    ## LAUNCH ACTIVE SCAN ##
    scan_id = start_ascan(url)
    progress = int(status_ascan(scan_id))
    while progress < 90:
        print(f"Active Scan Progress: {progress}")
        progress = int(status_ascan(scan_id))
        sleep(2)
    
    print("printing results")
    print(get_results(url))



if __name__ in '__main__':
    zap = "http://localhost:5000"
    try:
        url = argv[1]
        main(url)
    except Exception:
        print(f"Usage:\n\t {argv[0]} <url>")