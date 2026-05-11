from flask import Flask, Response
from prometheus_client import Counter, generate_latest
import time
import random

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total App HTTP Requests",
    ["method", "endpoint"]
)

@app.route("/fast")
def fast():
    REQUEST_COUNT.labels(method="GET", endpoint="/fast").inc()
    return {
        "status": "success",
        "message": "Fast endpoint response"
    }


@app.route("/slow")
def slow():
    REQUEST_COUNT.labels(method="GET", endpoint="/slow").inc()
    time.sleep(3)

    return {
        "status": "success",
        "message": "Slow endpoint response"
    }


@app.route("/error")
def error():
    REQUEST_COUNT.labels(method="GET", endpoint="/error").inc()
    return {
        "status": "failure",
        "message": "Simulated server error"
    }, 500


@app.route("/cpu")
def cpu():
    REQUEST_COUNT.labels(method="GET", endpoint="/cpu").inc()
    total = 0

    for i in range(10000000):
        total += i * i

    return {
        "status": "success",
        "message": "CPU intensive task completed"
    }


@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    return {
        "message": "AI Performance Incident Investigator Backend Running"
    }

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)