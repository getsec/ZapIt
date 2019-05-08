import flask
import requests
import json
import os
from urllib.parse import urlparse
from flask import request, abort, render_template
import flask_pure
import logging


app = flask.Flask(__name__)
app.config['PURECSS_RESPONSIVE_GRIDS'] = True
app.config['PURECSS_USE_CDN'] = True
app.config['PURECSS_USE_MINIFIED'] = True
flask_pure.Pure(app)
logger = logging.getLogger()
logging.basicConfig(
    format='%(asctime)s:%(levelname)s:%(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG
)

remote_host = logging.handlers.SysLogHandler(
    address=('10.111.5.122', 514))
logger.addHandler(remote_host)
logger.setLevel(logging.INFO)

try:
    ZAP_PORT = os.environ["ZAP_PORT"]
    ZAP_URL = os.environ["ZAP_URL"]
except KeyError:
    ZAP_URL = 'http://10.100.92.156'
    ZAP_PORT = '1337'

# TODO: Setup URL for passive scans
# TODO: Setup URL for active scans

ZAP_SPIDER_SCAN = '/JSON/spider/action/scan'
ZAP_SPIDER_STATUS = '/JSON/spider/view/status'
ZAP_SPIDER_RESULTS = '/JSON/spider/view/results'

zap_scan_spider_uri = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_SCAN}"
zap_scan_spider_status = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_STATUS}"
zap_scan_spider_results = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_RESULTS}"
# /END ZAP URLS


# TODO: Ensure logic in start scan api call actually registers the target
def register_target(zap_register_target_uri, target):
    post_data = {
        "target": target
    }
    data = requests.post(zap_register_target_uri,
                         data=post_data)
    if data.status_code == 200:
        logger.info(f"msg='registed target for scanning' target='{target}'")
        return target


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
        logger.info(f"msg='Scan succesfully launched' target='{requested_url}'")
        return data.content
    else:
        logger.error(f"msg='Scan initation failed' target='{data.content}'")
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
        logger.error(f"msg='returned non-200' error='{zap_scan_spider_status}'")
        logger.error(progress.status_code, progress.content)


def post_scan_results(zap_scan_spider_results, scan_id, format):
    post_data = {
        'zapapiformat': 'JSON',
        'formMethod': format,
        'scanId': scan_id
    }
    results = requests.post(zap_scan_spider_results, data=post_data)
    return results.content


# BEGIN API CALLS
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/easter", methods=["GET"])
def docs():
    return "</h1> eggies </h1>"


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
                logger.info(f"msg='User used restricted URL' target='{requested_url}") # NOQA
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
            results = post_scan_results(zap_scan_spider_results,
                                        scan_id,
                                        format)
            content = json.loads(results.decode('utf-8'))
            total_results = len(content['results'])
            u = urlparse(content['results'][0])
            base = f"{u.scheme}//{u.netloc}"

            logger.info(f"msg='Total Results' target='{base}' results='{total_results}'")
            f"msg='Total Results' target='{base}' results='{total_results}'"
            return results
        else:
            return msg
    except KeyError:
        return msg


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    logger.info(f"msg='Succesfully started' target='{ZAP_URL}:{ZAP_PORT}'")
    print(f"msg='Succesfully started' target='{ZAP_URL}:{ZAP_PORT}'")

