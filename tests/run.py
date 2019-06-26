import requests
import time
from os import environ
from colorama import Fore, Back, Style


domain = "https://example.com"


try:
    ZAP_PORT = environ["ZAP_PORT"]
    ZAP_URL = environ["ZAP_URL"]
    ZAP_URI = f"{ZAP_URL}:{ZAP_PORT}"
except KeyError:
    ZAP_URL = "http://localhost"
    ZAP_PORT = "5000"
    ZAP_URI = f"{ZAP_URL}:{ZAP_PORT}"


def logs(result, msg):
    if result is True:
        print(f"{Fore.GREEN}PASS: {Style.RESET_ALL}{msg}")
    if result is False:
        print(f"{Fore.RED}FAIL: {Style.RESET_ALL}{msg}")


def initiate_scan(domain):
    print("\nIntitate Scan Test.")
    r = requests.post(
        f"{ZAP_URI}/api/v1/spider/start",
        json={
            'url': domain
    })
    if r.ok:
        scan_id = r.json()['scan']
        msg = f"{ZAP_URI}/api/v1/spider/start - Launched Scan"
        result = True
        logs(result, msg)
        return scan_id
    else:
        msg = f"{ZAP_URI}/api/v1/spider/start - Non 200 Status Code"
        result = False
        logs(result, msg)


def check_spider_progress(scan_id):
    print("\nCheck Progress Test")
    while True:
        try:
            progres = 0
            r = requests.post(
                f"{ZAP_URI}/api/v1/spider/progress",
                json={
                    'id': scan_id
                }
            )
            if r.ok:
                if int(r.json()['status']) > 90:
                    msg = f"{ZAP_URI}/api/v1/spider/progress - over 90%. Good enough"
                    result = True
                    logs(result, msg)
                    break
            else:
                print("Non 200 code")
        except Exception as msg:
            print(f"FAIL: {msg}")


def check_spider_results(scan_id):
    print("\nCheck Spider Results Test.")
    try:
        req = requests.post(
            f"{ZAP_URI}/api/v1/spider/results",
            json={
                'id': scan_id
            }
        )
        if len(req.json()['results']) > 1:
            result = True
            msg = f"{ZAP_URI}/api/v1/spider/results - Results found"
            logs(result, msg)
        else:
            result = False
            msg = f"{ZAP_URI}/api/v1/spider/results - No results found. Ensure no issues"
            logs(result, msg)
    except Exception as msg:
        msg = str(msg)
        result = False
        logs(result, msg)


def check_scan_results(scan_id):
    print("\nCheck Scan Results Test.")
    req = requests.get(
        f"{ZAP_URI}/api/v1/scan/results"
    )
    #print(len(req.json()['site']))
    if len(req.json()['site']) > 0:
        msg = f"{ZAP_URI}/api/v1/scan/results - no issues"
        result = True
        logs(result, msg)
    else:
        print(req.json())
        msg = f"{ZAP_URI}/api/v1/scan/results - No generated results found"
        result = False
        logs(result, msg)


if __name__ == '__main__':
    scan_id = initiate_scan(domain)
    check_spider_progress(scan_id)
    check_spider_results(scan_id)
    check_scan_results(scan_id)
