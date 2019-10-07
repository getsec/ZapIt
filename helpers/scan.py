import requests
from pprint import pprint as pprint
from time import sleep
import yaml, json, sys
from sys import argv
import click
from helpers.redirect import get_redirect_url
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3 needed.
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
zap = "http://localhost:5000"
def write_file(results, filename, ext):
    
    if ext.lower() == 'json':
        with open(f'{filename}.json', 'w') as outfile:
            json.dump(results, outfile)

    elif ext.lower() == 'yaml':
        
        with open(f'{filename}.yml', 'a') as outfile:
            yaml.dump(results, outfile)


def start_spider(url):
    payload = {"url": get_redirect_url(url)}
    api_url = f"{zap}/api/v1/spider/start"
    r = requests.post(api_url, json=payload)
    return r.json()['scan_id']


def status_spider(scan_id):
    payload = {"scan_id": scan_id}
    api_url = f"{zap}/api/v1/spider/status"
    r = requests.post(api_url, json=payload)
    status_integer = int(r.json()['status'])
    return status_integer


def start_ascan(url):
    payload = {"url": url}
    api_url = f"{zap}/api/v1/active/scan"
    r = requests.post(api_url, json=payload)
    return r.json()['scan_id']


def status_ascan(scan_id):
    payload = {"scan_id": scan_id}
    api_url = f"{zap}/api/v1/active/status"
    r = requests.post(api_url, json=payload)
    print(f"ascan_status: {r.json()}")

    return int(r.json())


def results_spider(scan_id):
    payload = {"scan_id": scan_id}
    api_url = f"{zap}/api/v1/spider/results"
    r = requests.post(api_url, json=payload)
    return r.json()


def get_results(url):
    payload = {"url": url}
    api_url = f"{zap}/api/v1/results/summary"
    r = requests.post(api_url, json=payload)
    return r.json()
