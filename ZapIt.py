from pprint import pprint as pprint
from time import sleep
import argparse
from colorama import Fore, Style, init

from helpers.scan import (
    start_spider,
    start_ascan,
    results_spider,
    status_ascan,
    status_spider,
    get_results,
    write_file,
    update_ua
)

init()  # initialize colorama
## Load argument parser
parser = argparse.ArgumentParser()
parser.add_argument("url", help="full URL of the endpoint you wish to scan")
parser.add_argument(
    "--mode",
    default="normal",
    help="Which type of scan are we doing today [normal|spider|overkill]",
)
parser.add_argument(
    "--ua",
    default="ZapIt / Default User Agent",
    help="Updates the user agent to whatever you please",
)
args = parser.parse_args()

# Suppress only the single warning from urllib3 needed.
# requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


def banner(banner_params):
    banner = f"""{Fore.GREEN}
    _____          ___ _.
   |__  /__ _ _ __|_ _| |_
     / // _` | '_ \| || __|
    / /| (_| | |_) | || |_
   /____\__,_| .__/___|\__|
             |_| {Style.RESET_ALL}  

  {Fore.MAGENTA}OWASP ZAP CI/CD TESTING TOOL{Style.RESET_ALL}
 ** Actively in development. **
 **  need help?              **
 **         ZapIt.py --help  **
 ** ~~~~~~~~~~~~~~~~~~~~~~~~ **
    
    Your options are as follows:
"""  # NOQA
    print(banner)
    print
    for k, v in banner_params.items():
        print(f"\t{Fore.GREEN}{k}{Style.RESET_ALL}: {v}")
    return banner


def normal_mode(url):
    # Initiate spider
    scan_id = start_spider(url)
    progress = status_spider(scan_id)
    # while spider progress is less than 95%
    # complete, continue to scan
    print(f"Launching Spider Scan.")
    while progress < 95:
        progress = status_spider(scan_id)
        sleep(1)

    # Once the spider completes (mostly)
    # we will kick off the active scan
    print(f"Launching Active Scan.")
    scan_id = start_ascan(url)
    while progress < 95:
        progress = status_ascan(scan_id)
        sleep(1)

    print("Scan Completed. Results below\n")
    results = get_results(url)
    pprint(results)
    return results


def spider_mode(url):
    scan_id = start_spider(url)
    progress = status_spider(scan_id)
    # while spider progress is less than 95%
    # complete, continue to scan
    print(f"Launching Spider Scan.")
    while progress < 100:
        progress = status_spider(scan_id)
        sleep(1)
    sleep(1)
    spider_results = results_spider(scan_id)
    pprint(spider_results)
    return spider_results


if __name__ in "__main__":

    url = args.url
    filename = url.split("//")[1]
    banner_params = {"URL": url}
    banner_params.update({"Mode": args.mode})

    if args.ua:
        ua = args.ua
        banner_params.update({"User Agent": ua})
        update_ua(args.ua)

    banner(banner_params)

    if args.mode.lower() == "normal":
        scan_output = normal_mode(url)
        results = scan_output
        filename = 'ZapIt-normal-' + filename

    elif args.mode.lower() == "spider":
        scan_output = spider_mode(url)
        results = scan_output
        filename = 'ZapIt-spider-' + filename

    elif args.mode.lower() == "overkill":
        print("Overkill implmentation to be done later")

    write_file(results, filename)

