import requests
from time import sleep
from sys import argv
from helpers.redirect import get_redirect_url
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

def start_spider(url):

    payload = {
        "url": get_redirect_url(url)
    }
    r = requests.post(
        f"{zap}/api/v1/spider/start",
        json=payload
    )
    return r.json()

def status_spider(scan_id):
    payload = {
        "scan_id": scan_id
    }
    r = requests.post(
        f"{zap}/api/v1/spider/status",
        json=payload
    )
    return int(r.json()['status'])

def results_spider(scan_id):
    payload = {
        "scan_id": scan_id
    }
    r = requests.post(
        f"{zap}/api/v1/spider/results",
        json=payload
    )
    return r.json()



if __name__ in '__main__':
    zap = "http://localhost:5000"
    try:
        url = argv[1]
        print("Launching spider")
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


    except Exception:
        print(f"Usage:\n\t {argv[0]} <url>")