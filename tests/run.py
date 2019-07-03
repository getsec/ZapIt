import requests
import time
from os import environ
from colorama import Fore, Back, Style

# TODO: Clean this up and document
domain = "https://example.com"


API_URI = "http://127.0.0.1:5000"


def logs(result, msg):
    if result is True:
        print(f"{Fore.GREEN}PASS: {Style.RESET_ALL}{msg}")
    if result is False:
        print(f"{Fore.RED}FAIL: {Style.RESET_ALL}{msg}")


def initiate_scan(domain):
    print("\nIntitate Scan Test.")
    try:
        r = requests.post(
            f"{API_URI}/api/v1/spider/start",
            json={
                'url': domain
            })
        if r.ok:
            scan_id = r.json()['scan_id']
            msg = f"{API_URI}/api/v1/spider/start - Launched Scan"
            result = True
            logs(result, msg)
            return scan_id
        else:
            msg = f"{API_URI}/api/v1/spider/start - returned code '{r.status_code}'"
            result = False
            logs(result, r.content)
            logs(result, msg)
    except Exception as msg:
        result = False
        msg = str(msg)
        logs(result, msg)


def check_spider_progress(scan_id):
    print("\nCheck Progress Test")
    while True:
        try:
            # progres = 0
            r = requests.post(
                f"{API_URI}/api/v1/spider/progress",
                json={
                    'id': scan_id
                }
            )
            print(f"Progress: {r.json()['progress']}")
            if r.ok:
                if int(r.json()['progress']) > 90:
                    msg = f"{API_URI}/api/v1/spider/progress - over 90%. Good enough"
                    result = True
                    logs(result, msg)
                    break
            else:
                print("Non 200 code")
        except Exception as msg:
            result = False
            msg = f"Error loading spider progress uri: {API_URI}/api/v1/spider/progress"
            logs(result, msg)


def check_spider_results(scan_id):
    print("\nCheck Spider Results Test.")
    try:
        req = requests.post(
            f"{API_URI}/api/v1/spider/results",
            json={
                'id': scan_id
            }
        )
        if req.ok:
            result = True
            msg = f"{API_URI}/api/v1/spider/results - Results found"
            logs(result, msg)
        else:
            result = False
            msg = f"{API_URI}/api/v1/spider/results - No results found. Ensure no issues"
            logs(result, msg)
    except Exception as msg:
        msg = str(msg)
        result = False
        logs(result, msg)


def check_scan_results():
    print("\nCheck Scan Results Test.")
    req = requests.get(
        f"{API_URI}/api/v1/scan/results"
    )
    if req.ok:
        msg = f"{API_URI}/api/v1/scan/results - no issues"
        result = True
        logs(result, msg)
    else:
        print(req.json())
        msg = f"{API_URI}/api/v1/scan/results - No generated results found"
        result = False
        logs(result, msg)


if __name__ == '__main__':
    scan_id = initiate_scan(domain)
    check_spider_progress(scan_id)
    check_spider_results(scan_id)
    check_scan_results()
