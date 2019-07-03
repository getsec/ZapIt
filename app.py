
# Required libraries
import flask
import requests
import zapv2
from flask import (
    request,
    abort,
    jsonify,
    Response,
    render_template
)
# init flask & zap
app = flask.Flask(__name__)
zap = zapv2.ZAPv2(
    proxies={
        "http": "http://localhost:8080",
        "https": "https://localhost:8080"
    }
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


@app.route("/")
def home():
    """Loads the home page

    Returns:
        [obect] -- [template]
    """
    return render_template('home.html')


@app.route("/docs")
def docs():
    return """
    <meta http-equiv="refresh" content="0; URL='https://github.com/getsec/ZapIt/blob/master/docs/Documentation.md'"/>
    """


@app.route("/api/v1/spider/start", methods=["POST"])
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
    param = 'url'

    # If there is no JSON Response abort
    if not request.json:
        abort(400)
    try:
        # Ensure the url param was sent to the api
        if request.json['url']:
            #
            target = request.json['url']
            requested_url = get_redirect_url(target)
            app.logger.info(f"User requested URL: {target}")
            app.logger.info(f"URL Redirect: {requested_url}")

            scan_id = zap.spider.scan(
                url=requested_url,
                recurse=False
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
    """This function gets the progress of the current spider.
    Params:
        [dict] -- scan id dict
            {
                'id':'0'
            }
    Returns:
        [dict] -- [progress]
            {
                'progress':%ofprogress
            }
    """
    example_json = {"id": "#"}
    error = {
        "error": "incorrect payload syntax.",
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
                "progress": f'{scan_progress} %'
            }
            return jsonify(return_data)
        else:
            return jsonify(error)
    except KeyError:
        return jsonify(error)


@app.route("/api/v1/spider/results", methods=["POST"])
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


if __name__ in "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


