# Required libraries
import flask
import zapv2
import requests
from urllib.parse import urlparse
from flask import request, abort, jsonify, Response, render_template

# init flask & zap
api = flask.Flask(__name__)
zap = zapv2.ZAPv2(
    proxies={"http": "http://localhost:8080", "https": "https://localhost:8080"}
)


def get_redirect_url(target):
    """Takes in url, spits out redirect

    Arguments:
        target {str} -- requested url

    Returns:
        [str] -- url 302 redirect
    """
    r = requests.get(target, verify=False)
    return r.url


def naughty_url_check(target):
    """ Checks to make sure the URL is in a whitelist.
        Arguments:
            target {str} -- The URL
    """
    good_domains = ["example.com", "wawanesa.com"]
    if urlparse(target).netloc in good_domains:
        return True
    else:
        return False


@api.route("/")
def home():
    """Loads the home page

    Returns:
        [obect] -- [template]
    """
    return render_template("home.html")


@api.route("/docs")
def docs():
    return """
    <meta http-equiv="refresh" content="0; URL='https://github.com/getsec/ZapIt/blob/master/docs/Documentation.md'"/>
    """


@api.route("/api/v1/spider/start", methods=["POST"])
def spider_start():
    """[summary]

    Params:
        [dict] -- url dict
            {
                'url': 'http://example.com'
            }

    Returns:
        [str] -- [scan_id]
    """
    # Setting up some message for the response
    param = "url"
    error_param = {"error": f"Parameter '{param}' missing"}
    error_keyerror = {"error": 'Incorrect synaax. "{"url:"https://example.com"}'}
    error_restricted_url = {
        "error": "you are not authorized to scan the requested url."
    }
    # If there is no JSON Response abort
    if not request.json:
        abort(400)
    try:
        # Ensure the url param was sent to the api
        if request.json["url"]:
            target = request.json["url"]
            if naughty_url_check(target) is False:
                return jsonify(error_restricted_url), 401

            requested_url = get_redirect_url(target)
            scan_id = zap.spider.scan(url=requested_url, recurse=False, maxchildren=10)
            data = {"scan_id": scan_id}

            return jsonify(data)

        else:
            return jsonify(error_param)

    except KeyError:
        return jsonify(error_keyerror)


@api.route("/api/v1/spider/status", methods=["POST"])
def spider_progress():
    """This function gets the progress of the current spider.
    Params:
        [dict] -- scan id dict
            {
                'id':'0'
            }
    Returns:
        [dict] -- [progress]
            {
                'status':'#'
            }
    """
    example_json = {"id": "#"}
    error = {"error": "incorrect payload syntax.", "suggested_payload": example_json}
    # Ensure request includes json data
    if not request.json:
        return "No json found"
        abort(400)
    # ensure that the ID param is in the request
    try:
        if request.json["id"].isdigit():
            scan_id = request.json["id"]
            scan_progress = zap.spider.status(scanid=scan_id)
            return_data = {"status": scan_progress}
            return jsonify(return_data)
        else:
            return jsonify(error)
    except KeyError:
        return jsonify(error)


@api.route("/api/v1/spider/results", methods=["POST"])
def spider_results():
    """Dumps results of the spider
    Params:
        [dict] -- ID of the scan
            {
                'id': #
            }
    Returns:
        [dict] -- Big ol list of sites
    """

    example_json = {"id": "#"}
    error = {
        "error": f"incorrect request payload. use suggested payload",
        "suggested_payload": example_json,
    }

    if not request.json:
        abort(Response(error))

    try:
        if request.json["id"].isdigit():
            scan_id = request.json["id"]
            results = zap.spider.results(scanid=scan_id)

            return jsonify(results)
        else:
            return jsonify(error)
    except KeyError:
        return jsonify(error)


@api.route("/api/v1/scan/results", methods=["GET"])
def scan_results():
    """Returns all scan results

    Returns:
        [dict] -- All results found
    """
    # Returns full results.
    try:
        output = zap.alert.alerts()
        return jsonify(output)
    except Exception:
        return abort(500)


@api.route("/api/v1/scan/results/summary", methods=["GET"])
def scan_results_summary():
    """Returns all scan results

    Returns:
        [dict] -- All results found
    """
    summary = []
    # Returns a subset of results
    try:
        for alert in zap.alert.alerts():
            summary.append(
                {
                    "alert": alert.get("alert"),
                    "risk": alert.get("risk"),
                    "method": alert.get("method"),
                    "param": alert.get("param", "null"),
                    "evidence": alert.get("evidence", "null"),
                    "solution": alert.get("solution", "null"),
                }
            )
        # used for getting unique list of items based off evidence value.
        output = list({v["evidence"]: v for v in summary}.values())
        return jsonify(output)
    except Exception:
        return abort(500)


if __name__ in "__main__":
    api.run(host="0.0.0.0", port=5000, debug=True)

