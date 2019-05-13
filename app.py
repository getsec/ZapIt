import flask
import requests
from sys import exit
from os import environ
from urllib.parse import urlparse
from flask import request, abort, jsonify
import logging


app = flask.Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Attempt to load the required params from env.
# These should be loaded from the docker deploy script
try:
    ZAP_PORT = environ["ZAP_PORT"]
    ZAP_URL = environ["ZAP_URL"]
except KeyError:
    error = "Could not get environment variables ZAP_URL or ZAP_PORT"
    exit(error)

# Used to enable passive scans, and launches spider
def register_and_scan(ZAP_URL, ZAP_PORT, requested_url):
    ZAP_SPIDER_SCAN = '/JSON/spider/action/scan'
    ZAP_REGISTER = "/JSON/pscan/action/setEnabled"
    zap_register_target_uri = f"{ZAP_URL}:{ZAP_PORT}{ZAP_REGISTER}"
    zap_scan_spider_uri = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_SCAN}"
    register = requests.post(
        zap_register_target_uri,
        data={
            "zapapiformat": "JSON",
            "formMethod": "POST",
            "enabled": "True"
        }
    )
    if register.status_code == 200:
        logger.info(f"msg='Scan succesfully launched' target='{requested_url}'")
    else:
        logger.error(f"msg='Scan initation failed' target='{register.content}'")

    post_data = {
        'zapapiformat': 'JSON',
        'formMethod': 'POST',
        'url': requested_url,
        'maxChildren': '',
        'recurse': 'True',
        'contextName': '',
        'subtreeOnly': ''
    }

    data = requests.post(zap_scan_spider_uri, data=post_data)
    if data.status_code == 200:
        logger.info(f"msg='Scan succesfully launched' target='{requested_url}'")
        return data.json()

    else:
        abort(500)


# Used for getting the status of the spider.
def post_scan_status(ZAP_URL, ZAP_PORT, scan_id):
    ZAP_SPIDER_STATUS = '/JSON/spider/view/status'
    zap_scan_spider_status = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_STATUS}"
    post_data = {
        'zapapiformat': 'JSON',
        'formMethod': 'POST',
        'scanId': scan_id
    }
    progress = requests.post(zap_scan_spider_status, data=post_data)
    if progress.status_code == 200:
        return progress.json()
    else:
        logger.error(f"msg='returned non-200' error='{zap_scan_spider_status}'")
        logger.error(progress.status_code, progress.content)


# Used for downloading the results of the spider
def post_scan_results(ZAP_URL, ZAP_PORT, scan_id):
    ZAP_SPIDER_RESULTS = '/JSON/spider/view/results'
    zap_scan_spider_results = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_RESULTS}"
    post_data = {
        'zapapiformat': 'JSON',
        'formMethod': 'json',
        'scanId': scan_id
    }
    results = requests.post(zap_scan_spider_results, data=post_data)
    return results.json()


# Used for downloading the entire report
# This will send back passive scan results.
def full_report(ZAP_URL, ZAP_PORT):
    ZAP_SCAN_RESULTS = "/OTHER/core/other/jsonreport/?formMethod=GET"
    zap_vulnerability_results = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SCAN_RESULTS}"
    results = requests.get(zap_vulnerability_results)
    if results.status_code == 200:
        return results.json()
    else:
        return "Error rendering request"


# BEGIN API CALLS
@app.route("/")
def home():
    welcome = """
        <h1>
            Welcome Friends
        </h1>

        <p>
            Hey There. I'm sure you are looking for some documentation. No problem. I got
                <a href="https://github.com/getsec/ZapIt"> you</a>
        </p>
    """
    return welcome


@app.route("/api/v1/spider/start", methods=["POST"])
def spider_start():
    # Setting up some message for the response
    param = 'url'
    acceptance_strings = [
        'wmic.ins',
        'wawanesa.com',
        'example.com'
    ]
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
            for match in acceptance_strings:
                if requested_url.endswith(match):
                    scan_id = register_and_scan(ZAP_URL, ZAP_PORT, requested_url)
                    return jsonify(scan_id)
            else:
                # if not return the error to the user
                logger.info(f"msg='User used restricted URL' target='{requested_url}") # NOQA
                return resrict.format(requested_url)

        else:
            return f"No {param} Parameter passed"
    except KeyError:
        return f"Incorrect synax. Please post: \n{example_json}"


@app.route("/api/v1/spider/progress", methods=["POST"])
def spider_progress():
    param = 'id'
    example_json = "{\n  \"id\":\"4\"\n}"
    # Ensure request includes json data
    if not request.json:
        return "No json found"
        abort(400)
    # ensure that the ID param is in the request
    try:
        if request.json['id']:
            scan_id = request.json['id']
            scan_progress = post_scan_status(ZAP_URL, ZAP_PORT, scan_id)
            return jsonify(scan_progress)
        else:
            return f"No {param} Parameter passed"
    except KeyError:
        return f"Incorrect synax.\nmethod = POST\nexample \n{example_json}"


@app.route("/api/v1/spider/results", methods=["POST"])
def spider_results():
    example_json = "{\n  \"id\":\"2\"\n}"
    msg = f"missing id or format param in request\n\n{example_json}"
    if not request.json:
        abort(400)

    try:
        if request.json['id']:
            scan_id = request.json['id']
            results = post_scan_results(ZAP_URL, ZAP_PORT, scan_id)
            total_results = len(results['results'])
            u = urlparse(results['results'][0])
            base = f"{u.scheme}//{u.netloc}"

            logger.info(f"msg='Total Results' target='{base}' results='{total_results}'")
            f"msg='Total Results' target='{base}' results='{total_results}'"
            return jsonify(results)
        else:
            return msg
    except KeyError:
        return msg


@app.route("/api/v1/scan/results", methods=["GET"])
def scan_results():
    # Returns full results.
    try:
        output = full_report(ZAP_URL, ZAP_PORT)
        return jsonify(output)
    except Exception:
        return abort(500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    logger.info(f"msg='Succesfully started' target='{ZAP_URL}:{ZAP_PORT}'")
    print(f"msg='Succesfully started' target='{ZAP_URL}:{ZAP_PORT}'")
