# ZAPiT API Examples

TODO: Add some description

# REST API

The REST API to the example app is described below.

## Inititate Spider

### Request

`POST /api/v1/spider/start`
```sh
curl -i -H 'Content-Type: application/json' \ 
    -d '{"url":"https://example.com"}' \ 
    http://localhost:5000/api/v1/spider/start 
```
### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json

    {"scan":"0"}

## Check Spider Status

### Request

`POST /api/v1/spider/status`
```sh
curl -i -H 'Content-Type: application/json' \ 
    -d '{"scan":"0"}' \ 
    http://localhost:5000/api/v1/spider/status 
```
### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json

    {"progress":"67"}

## Download Report

### Request
> *Scan progress should be atleast 99 for max results*

`POST /api/v1/spider/report`
```sh
curl -i -H 'Content-Type: application/json' \ 
    -d '{"scan":"0", "format":"json"}' \ 
    http://localhost:5000/api/v1/spider/report 
```
### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json

    {large json object}