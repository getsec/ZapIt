from fastapi import FastAPI
import zapv2
from os import environ
from helpers.redirect import get_redirect_url

from pydantic import BaseModel

FastAPI()
tool_name = "Wawanesa ZapIt CI\CD Scanning Tool"

app = FastAPI(
    title=tool_name,
    description="CICD Tool for scanning webapps in the pipeline")  # initialize the API

zap = zapv2.ZAPv2(
    proxies={
        "http": environ['ZAP'],
        "https": environ['ZAPTLS']
    }
)
class Spider(BaseModel):
    url: str
    
class SpiderStatus(BaseModel):
    scan_id: str


@app.post("/api/v1/spider/start")
def spider(params: Spider):
    scan_id = zap.spider.scan(
        url=params.url,
        recurse=False, 
        maxchildren=10
    )
    return {"scan_id": scan_id}



@app.post("/api/v1/spider/status")
def spider_status(params: SpiderStatus):
    scan_id = params.scan_id
    return {
        "status": zap.spider.status(scanid=scan_id)
    }

@app.post("/api/v1/spider/results")
def spider_results(params: SpiderStatus):
    scan_id = params.scan_id
    return zap.spider.results(scanid=scan_id)
