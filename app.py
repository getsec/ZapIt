import flask
import requests
from flask import request, abort, render_template
import logging


app = flask.Flask(__name__)
logger = logging.getLogger()
logger.setLevel(logging.INFO)
# TODO: Figure out logging.


# ZAP INFORMATION
ZAP_URL = 'http://10.100.92.156'  # TODO: replace with environment variable
ZAP_PORT = '1337'   # TODO: replace with environment variable
ZAP_SPIDER_SCAN = '/JSON/spider/action/scan'
ZAP_SPIDER_STATUS = '/JSON/spider/view/status'
ZAP_SPIDER_RESULTS = '/JSON/spider/view/results'

zap_scan_spider_uri = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_SCAN}"
zap_scan_spider_status = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_STATUS}"
zap_scan_spider_results = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_RESULTS}"


def post_scan_start(zap_scan_spider_uri, requested_url):
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
        logger.info(f"Scan succesfully launched against {requested_url}")
        return data.content
    else:
        logger.error(f"Scan initation failed {data.content}")
        return data.content


def post_scan_status(zap_scan_spider_status, scan_id):
    post_data = {
        'zapapiformat': 'JSON',
        'formMethod': 'POST',
        'scanId': scan_id
    }
    progress = requests.post(zap_scan_spider_status, data=post_data)
    if progress.status_code == 200:
        return progress.content
    else:
        logger.error(f"{zap_scan_spider_status} returned non-200")
        logger.error(progress.status_code, progress.content)


def post_scan_results(zap_scan_spider_results, scan_id, format):
    post_data = {
        'zapapiformat': 'JSON',
        'formMethod': format,
        'scanId': scan_id
    }
    results = requests.post(zap_scan_spider_results, data=post_data)
    return results.content


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/api/v1/scan/start", methods=["POST"])
def spider_start():
    # Setting up some message for the response
    param = 'url'
    acceptance_strings = [
        'wmic.ins',
        'wawanesa.com'
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
                    scan_id = post_scan_start(zap_scan_spider_uri,
                                              requested_url)
                    return scan_id
            else:
                # if not return the error to the user
                return resrict.format(requested_url)
        else:
            return f"No {param} Parameter passed"
    except KeyError:
        return f"Incorrect synax. Please post: \n{example_json}"


@app.route("/api/v1/scan/progress", methods=["POST"])
def spider_progress():
    param = 'id'
    example_json = "{\n  \"id\":\"4\"\n}"
    if not request.json:
        abort(400)
    try:
        if request.json['id']:
            scan_id = request.json['id']
            scan_progress = post_scan_status(zap_scan_spider_status,
                                             scan_id)
            return scan_progress
        else:
            return f"No {param} Parameter passed"
    except KeyError:
        return f"Incorrect synax.\nmethod = POST\nexample \n{example_json}"


@app.route("/api/v1/scan/results", methods=["POST"])
def spider_results():
    example_json = "{\n  \"format\":\"json\", \"id\":\"2\"\n}"
    msg = f"missing id or format param in request\n\n{example_json}"
    if not request.json:
        abort(400)

    try:
        if request.json['id'] and request.json['format']:
            scan_id = request.json['id']
            format = request.json['format'].upper()
            spider_results = post_scan_results(zap_scan_spider_results,
                                               scan_id,
                                               format)
            return spider_results
        else:
            return msg
    except KeyError:
        return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
