import flask
import requests
from flask import request, jsonify, abort, render_template

app = flask.Flask(__name__)

# ZAP INFORMATION
ZAP_URL = 'http://10.100.92.156'
ZAP_PORT = '1337'
ZAP_SPIDER_SCAN = '/JSON/spider/action/scan'


zap_scan_spider_uri = f"{ZAP_URL}:{ZAP_PORT}{ZAP_SPIDER_SCAN}"


def post_scan_start(zap_scan_spider_uri, requested_url):
    post_data = {
        'zapapiformat': 'JSON',
        'formMethod': 'POST',
        'url': requested_url,  # FIXME: You need to URL encode this parameter
        'maxChildren': 1,
        'recurse': 'False',
        'contextName': '',
        'subtreeOnly': 'None'
    }
    data = requests.post(zap_scan_spider_uri, data=post_data)
    # print(post_data)
    # print(data.content)
    return data.content


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/api/v1/scan/start", methods=["POST"])
def scan_start():

    # Setting up some message for the response
    param = 'url'
    acceptance_strings = [
        'wmic.ins',
        '.ins'
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
            print(f"URL = {requested_url}")
            # Ensure that the url is within the whitelist
            for bad_string in acceptance_strings:
                if bad_string in request.json['url']:
                    scan_results = post_scan_start(zap_scan_spider_uri,
                                                   requested_url)
                    return scan_results
                else:
                    # if not return the error to the user
                    return resrict.format(requested_url)
        else:
            return f"No {param} Parameter passed"
    except KeyError:
        return f"Incorrect synax. Please post: \n{example_json}"


@app.route("/api/v1/scan/progress", methods=["POST"])
def scan_progress():
    param = 'id'
    example_json = "{\n  \"id\":\"4\"\n}"
    if not request.json:
        abort(400)
    print(f"input: {request.json}")
    try:
        if request.json['id']:
            output = {
                param: request.json[param]
            }
            return jsonify(output)
        else:
            return f"No {param} Parameter passed"
    except KeyError:
        return f"Incorrect synax.\nmethod = POST\nexample \n{example_json}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
