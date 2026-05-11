from flask import Flask, Response
from prometheus_client import Counter, generate_latest, Histogram
import time
import subprocess
import os
import shutil
from parser import parse_jmeter_results

app = Flask(__name__)

REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total App HTTP Requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds",
    "Request latency",
    ["method", "endpoint"]
)

ERROR_COUNT = Counter(
    "app_errors_total",
    "Total App Errors",
    ["method", "endpoint"]
)

@app.route("/fast")
def fast():
    REQUEST_COUNT.labels(method="GET", endpoint="/fast").inc()

    with REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/fast"
    ).time():

        return {
        "status": "success",
        "message": "Fast endpoint response"
        }


@app.route("/slow")
def slow():
    REQUEST_COUNT.labels(method="GET", endpoint="/slow").inc()

    with REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/slow"
    ).time():

        time.sleep(2)
        return {
        "status": "success",
        "message": "Slow endpoint response"
        }


@app.route("/error")
def error():
    REQUEST_COUNT.labels(method="GET", endpoint="/error").inc()

    ERROR_COUNT.labels(
        method="GET",
        endpoint="/error"
    ).inc()

    return {
        "status": "failure",
        "message": "Simulated server error"
    }, 500


@app.route("/cpu")
def cpu():
    REQUEST_COUNT.labels(method="GET", endpoint="/cpu").inc()

    with REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/cpu"
    ).time():

        total = 0

        for i in range(10000000):
            total += i * i

        return f"CPU work done: {total}"
        

@app.route("/")
def home():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    return {
        "message": "AI Performance Incident Investigator Backend Running"
    }

@app.route("/start-test")
def start_test():

    jmeter_command = [
        "jmeter",
        "-n",
        "-t",
        "/app/jmeter/testplans/basic_load_test.jmx",
        "-l",
        "/app/jmeter/results/results.jtl",
        "-e",
        "-o",
        "/app/jmeter/reports/html_report"
    ]

    report_path = "/app/jmeter/reports/html_report"

    if os.path.exists(report_path):
        shutil.rmtree(report_path)

    results_file = "/app/jmeter/results/results.jtl"

    if os.path.exists(results_file):
        os.remove(results_file)

    try:
        subprocess.run(jmeter_command, check=True)

        results = parse_jmeter_results(
            "/app/jmeter/results/results.jtl"
        )

        return {
            "status": "success",
            "message": "JMeter test completed",
            "results": results
        }

    except subprocess.CalledProcessError as e:

        return {
            "status": "failure",
            "message": str(e)
        }, 500

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)