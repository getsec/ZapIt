from fastapi import FastAPI
import zapv2
from os import environ
from helpers.redirect import get_redirect_url

# import all the parameters
from helpers.params import (
    DestinationHost,
    SpiderStatus
)

FastAPI()
tool_name = "Wawanesa ZapIt CICD Scanning Tool"

app = FastAPI(
    title=tool_name, description="CICD Tool for scanning webapps in the pipeline"
)  # initialize the API

zap = zapv2.ZAPv2(proxies={"http": environ["ZAP"], "https": environ["ZAPTLS"]})


@app.post("/api/v1/spider/start")
def spider(params: DestinationHost):
    """
        Launch a scan based off the url
    
    Arguments:
        url {str} -- [URL of the host]
    
    Returns:
        dict -- example:
            {"scan_id": "0"}
    """
    url = params.url
    redirected_url = get_redirect_url(url)
    scan_id = zap.spider.scan(url=redirected_url, recurse=False, maxchildren=10)
    return {"scan_id": scan_id}


@app.post("/api/v1/spider/status")
def spider_status(params: SpiderStatus):
    """
        This function will take the input and return
        the percentage of the spider scan progress
    
    Arguments:
        scan_id 
    
    Returns:
        [dict] -- percentage example:
                {"status":"90"}
    """
    scan_id = params.scan_id
    return {"status": zap.spider.status(scanid=scan_id)}


@app.post("/api/v1/spider/results")
def spider_results(params: SpiderStatus):
    """
        This function takes in the ID of the scan
        And will return a list of all the urls the
        spider found within the scan

    Arguments:
        scan_id -- ID from the start url
    
    Returns:
        [list] -- List of all urls
    """
    scan_id = params.scan_id
    return zap.spider.results(scanid=scan_id)


@app.post("/api/v1/results/summary")
def scan_results_summary(params: DestinationHost):
    """[summary]
    
    Arguments:
        url:
            function takes in url, redirects to the final url
            then will get a list of all the unique results
    
    Retuns:
        Unique set of results

    """
    url = DestinationHost.url
    redirected_url = get_redirect_url(url)
    full_zap_results = zap.alert.alerts(baseurl=redirected_url)
    summary = []
    
    for single_result in full_zap_results:
        summary.append(
            {
                "alert": single_result.get("alert"),
                "risk": single_result.get("risk"),
                "method": single_result.get("method"),
                "param": single_result.get("param", "null"),
                "evidence": single_result.get("evidence", "null"),
                "solution": single_result.get("solution", "null"),
            }
        )
    # used for getting unique list of items.
    output = list({v["evidence"]: v for v in summary}.values())

    return output

@app.post("/api/v1/results/full")
def scan_results_full():
    url = DestinationHost.url
    redirected_url = get_redirect_url(url)
    return zap.alert.alerts(baseurl=redirected_url)