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


@api.route("/api/v1/scan/results", methods=["POST"])
def scan_results_summary():
    """[summary]

    Params:
        [dict] -- url dict
            {
                'url': 'http://example.com'
            }

    Returns:
        [list of dicts] -- [{alerts}]
    """

    error_keyerror = {"error": 'Incorrect synaax. "{"url:"https://example.com"}'}
    error_restricted_url = {
        "error": "you are not authorized to request data for that url."
    }
    try:
        if request.json["url"]:
            target = request.json["url"]
            base_url = get_redirect_url(target)
            if naughty_url_check(target) is False:
                return jsonify(error_restricted_url), 401
        # Returns a subset of results
        try:
            summary = []
            for alert in zap.alert.alerts(baseurl=base_url):
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
    except KeyError:
        return jsonify(error_keyerror)


if __name__ in "__main__":
    api.run(host="0.0.0.0", port=5000, debug=True)

