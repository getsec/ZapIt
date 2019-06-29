import flask
import requests
from sys import exit
from os import environ
from urllib.parse import urlparse
from flask import (
    request, 
    abort, 
    jsonify, 
    Response
)
from flask import render_template
import logging
from zapv2 import ZAPv2

# These two need to be here. Dont ask me why
app = flask.Flask(__name__)
zap = ZAPv2()
TEMPLATES_AUTO_RELOAD = True

@app.route("/")
def home():
    return  render_template('home.html')



@app.route("/api/v1/spider/start", methods=["POST"])
def spider_start():
    # Setting up some message for the response
    param = 'url'

    resrict = "Resticted domain used in URL '{}'"
    example_json = "{\n  \"url\":\"https://xxx.com\"\n}"

    # If there is no JSON Response abort
    if not request.json:
        abort(400)
    try:
        # Ensure the url param was sent to the api
        if request.json['url']:
            requested_url = request.json['url']
            # Ensure that the url is within the whitelist

            scan_id = zap.spider.scan(
                url=requested_url,
                recurse=True
            )
            data = {"scan_id": scan_id}
            return jsonify(data)
        else:
            error = {
                "error": f"Parameter '{param}' missing"
            }
            return jsonify(error)
    except KeyError:
        error = {
            "error": "Incorrect synaax. \"{\"url:\"https://example.com\"}"
        }
        return jsonify(error)


@app.route("/api/v1/spider/progress", methods=["POST"])
def spider_progress():
    param = 'id'
    example_json = {"id" : "#"}
    error = {
        "error": f"incorrect request payload. use suggested payload",
        "suggested_payload": example_json
    }
    # Ensure request includes json data
    if not request.json:
        return "No json found"
        abort(400)
    # ensure that the ID param is in the request
    try:
        if request.json['id'].isdigit():
            scan_id = request.json['id']
            scan_progress = zap.spider.status(
                scanid=scan_id
            )
            return_data = {
                "progress": scan_progress
            }
            return jsonify(return_data)
        else:
            return jsonify(error)
    except KeyError:
        return jsonify(error)


@app.route("/api/v1/spider/results", methods=["POST"])
def spider_results():
    example_json = {"id":"#"}
    error = {
        "error": f"incorrect request payload. use suggested payload",
        "suggested_payload": example_json
    }
    
    if not request.json:
        abort(Response(error))

    try:
        if request.json['id'].isdigit():
            scan_id = request.json['id']
            results = zap.spider.results(
                scanid=scan_id
            )

            return jsonify(results)
        else:
            return jsonify(error)
    except KeyError:
        return jsonify(error)


@app.route("/api/v1/scan/results", methods=["GET"])
def scan_results():
    # Returns full results.
    try:
        output = zap.alert.alerts()
        return jsonify(output)
    except Exception:
        return abort(500)


if __name__ == '__main__':
    

    # load env vars
    # these should be exported from the deploy script.
    try:
        ZAP_PORT = '8080' # environ["ZAP_PORT"]
        ZAP_URL = 'http://127.0.0.1' # environ["ZAP_URL"]
    except KeyError as msg:
        error = "issue loading env - check log for more"
        exit(error)
    

    app.run(host='0.0.0.0', port=5000, debug=True)
