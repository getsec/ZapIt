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
ASCAN = f"{zap}/api/v1/active/scan"
ASCAN_STATUS = f"{zap}/api/v1/active/status"
SPIDER = f"{zap}/api/v1/spider/start"
SPIDER_STATUS = f"{zap}/api/v1/spider/status"
SPIDER_RESULTS = f"{zap}/api/v1/spider/results"
TOTAL_RESULTS = f"{zap}/api/v1/results/summary"
UPDATE_UA = f"{zap}/api/v1/results/summary"

def write_file(results, filename, ext):
    
    if ext.lower() == 'json':
        with open(f'{filename}.json', 'w') as outfile:
            json.dump(results, outfile)

    elif ext.lower() == 'yaml':
        
        with open(f'{filename}.yml', 'a') as outfile:
            yaml.dump(results, outfile)


def start_spider(url):
    payload = {"url": get_redirect_url(url)}
    r = requests.post(SPIDER, json=payload)
    return r.json()['scan_id']


def status_spider(scan_id):
    payload = {"scan_id": scan_id}
    r = requests.post(SPIDER_STATUS, json=payload)
    #print(r.json())
    status_integer = int(r.json()['status'])
    return status_integer


def start_ascan(url):
    payload = {"url": url}
    r = requests.post(ASCAN, json=payload)
    return r.json()['scan_id']


def status_ascan(scan_id):
    payload = {"scan_id": scan_id}
    r = requests.post(ASCAN_STATUS, json=payload)
    print(f"ascan_status: {r.json()}")
    return int(r.json())


def results_spider(scan_id):
    payload = {"scan_id": scan_id}
    r = requests.post(SPIDER_RESULTS, json=payload)
    return r.json()


def get_results(url):
    payload = {"url": url}
    r = requests.post(TOTAL_RESULTS, json=payload)
    return r.json()

def update_ua(ua):
    payload = {"ua": ua}
    r = requests.post(UPDATE_UA, json=payload)
    return r.json()