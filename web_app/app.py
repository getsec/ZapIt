import flask
import json
from flask import request, jsonify, abort

app = flask.Flask(__name__)


# Test Data
test_data = [
    {"id": 0, "name": "A Fire Upon the Deep", "cat": "Vernor Vinge"},
    {"id": 0, "name": "A reddit Upon the Deep", "cat": "chocolate Vinge"},
    {"id": 0, "name": "gmail", "cat": "axe Vinge"}
]


@app.route("/", methods=["GET"])
def home():
    return "<h1>G3 PT API</h1><p>This site is a prototype API</p>"


@app.route("/api/v1/scan/start", methods=["POST"])
def scan_start():
    example_json = "{\n  \"url\":\"https://xxx.com\"\n}"
    if not request.json:
        abort(400)
    print(f"input: {request.json}")
    try:
        if request.json['url']:
            output = {"url": request.json['url']}
            # TODO: Post this to ZAP
            return jsonify(output)
        else:
            return "No URL Parameter passed"
    except KeyError:
        return f"Incorrect synax. Please post: \n{example_json}"



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
