import argparse
from flask import Flask, Response, render_template, request
import requests
import logging
import sys


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default=8000)
    parser.add_argument("--host", default="0.0.0.0")
    return parser.parse_args()


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/classify-sentiment")
def classify_sentiment():
    return render_template("lingofunk-classify-sentiment.html")


@app.route("/api/classifier/activations")
def activations_api():
    msg = f"Got {request.get_json()}, resent to the worker."
    logger.debug(msg)
    response = requests.post(
        "http://sentiment-classifier:8000/activations", json=request.get_json()
    )
    return Response(response.content, response.status_code)


# # todo: make all demos generic
# @app.route('/worker_demo')
# def worker_demo():
#     return render_template('worker_demo.html')


# # todo: make worker_one generic argument and redirect blindly
# @app.route('/api/worker_one/vectorize', methods=['POST'])
# def api_worker():
#     msg = 'API proxy got {} resend to worker'.format(request.get_json())
#     logger.debug(msg)
#     response = requests.post(
#         'http://worker_one:8000/vectorize',
#         json=request.get_json())
#     return Response(response.content, response.status_code)


if __name__ == "__main__":
    args = _parse_args()
    app.run(**args.__dict__)
