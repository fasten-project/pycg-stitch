import json

from flask import Flask, jsonify, request
from stitcher.stitcher import Stitcher


app = Flask(__name__)


@app.route("/stitch")
def hello():
    content = request.json

    stitcher = Stitcher([], False)
    for cg in content.values():
        stitcher.parse_cg(cg)
    stitcher.stitch()

    output = json.dumps(stitcher.output())

    return output


def deploy(host='0.0.0.0', port=5000):
    app.run(threaded=True, host=host, port=port)
