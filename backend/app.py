from flask import Flask, Response, request, render_template, jsonify
from prometheus_client import Counter, generate_latest, Histogram, Gauge
import time
import subprocess
import os
import shutil
from parser import parse_jmeter_results
from incidents import analyze_incident
from dotenv import load_dotenv
from ai_analyzer import generate_ai_analysis
from prometheus_metrics import get_system_metrics
from urllib.parse import urlparse
import random
import json
from datetime import datetime

load_dotenv()

app = Flask(__name__)

latest_test_result = {}

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

TEST_AVG_LATENCY = Gauge(
    "load_test_avg_latency_ms",
    "Average latency of latest load test"
)

TEST_ERROR_PERCENTAGE = Gauge(
    "load_test_error_percentage",
    "Error percentage of latest load test"
)

TEST_THROUGHPUT = Gauge(
    "load_test_throughput_rps",
    "Throughput of latest load test"
)

TEST_TOTAL_REQUESTS = Gauge(
    "load_test_total_requests",
    "Total requests in latest load test"
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
    
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/start-test")
def start_test():

    base_url = request.args.get(
    "baseUrl",
    "http://localhost:5000"
    )

    parsed_url = urlparse(base_url)

    protocol = parsed_url.scheme
    host = parsed_url.hostname or "localhost"

    port = (
        parsed_url.port
        or (443 if protocol == "https" else 80)
    )

    path = request.args.get(
    "path",
    "/fast"
    )
    
    users = request.args.get(
    "users",
    "100"
    )

    rampup = request.args.get(
    "rampup",
    "10"
    )

    loops = request.args.get("loops", "5")

    timer = request.args.get("timer", "500")

    journey_endpoints = request.args.get(
    "journeyEndpoints",
    ""
    )

    journey_list = [
        endpoint.strip()
        for endpoint in journey_endpoints.splitlines()
        if endpoint.strip()
    ]

    if journey_list:
        path1 = journey_list[0] if len(journey_list) > 0 else "NONE"
        path2 = journey_list[1] if len(journey_list) > 1 else "NONE"
        path3 = journey_list[2] if len(journey_list) > 2 else "NONE"
    else:
        path1 = path
        path2 = "NONE"
        path3 = "NONE"

    jmeter_command = [
    "jmeter",
    "-n",
    "-t",
    "/app/jmeter/testplans/basic_load_test.jmx",

    "-Jusers=" + users,
    "-Jrampup=" + rampup,
    "-Jloops=" + loops,
    "-Jtimer=" + timer,

    "-Jprotocol=" + protocol,
    "-Jhost=" + host,
    "-Jport=" + str(port),

    "-Jpath1=" + path1,
    "-Jpath2=" + path2,
    "-Jpath3=" + path3,

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

        TEST_AVG_LATENCY.set(
            results["average_latency_ms"]
        )

        TEST_ERROR_PERCENTAGE.set(
            results["error_percentage"]
        )

        TEST_THROUGHPUT.set(
            results["throughput_rps"]
        )

        TEST_TOTAL_REQUESTS.set(
            results["total_requests"]
        )

        test_context = {
            "path": path,
            "users": users,
            "rampup": rampup,
            "loops": loops,
            "timer": timer
        }

        incidents = analyze_incident(results, test_context)

        system_metrics = get_system_metrics()

        ai_analysis = generate_ai_analysis(
            results,
            incidents,
            system_metrics,
            test_context
        )

        global latest_test_result

        latest_test_result = {
            "status": "success",
            "message": "JMeter test completed",
            "results": results,
            "incidents": incidents,
            "system_metrics": system_metrics,
            "ai_analysis": ai_analysis
        }

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        history_path = (
            f"/app/test_history/test_{timestamp}.json"
        )

        os.makedirs("/app/test_history", exist_ok=True)

        with open(history_path, "w") as file:
            json.dump(latest_test_result, file, indent=4)

        return latest_test_result

    except subprocess.CalledProcessError as e:

        return {
            "status": "failure",
            "message": str(e)
        }, 500


@app.route("/latest-result")
def latest_result():
    return latest_test_result

@app.route("/grafana")
def grafana():
    return render_template("grafana.html")

@app.route("/metrics")
def metrics():
    return Response(generate_latest(), mimetype="text/plain")

@app.route("/chaos/latency")
def chaos_latency():

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/chaos/latency"
    ).inc()

    with REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/chaos/latency"
    ).time():

        delay = random.uniform(1, 5)

        time.sleep(delay)

        return {
            "status": "success",
            "delay_seconds": round(delay, 2),
            "message": "Latency chaos injected"
        }

@app.route("/chaos/failure")
def chaos_failure():

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/chaos/failure"
    ).inc()

    failure_chance = random.random()

    if failure_chance < 0.5:

        ERROR_COUNT.labels(
            method="GET",
            endpoint="/chaos/failure"
        ).inc()

        return {
            "status": "failure",
            "message": "Injected random failure"
        }, 500

    return {
        "status": "success",
        "message": "Request succeeded"
    }

@app.route("/chaos/cpu")
def chaos_cpu():

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/chaos/cpu"
    ).inc()

    with REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/chaos/cpu"
    ).time():

        total = 0

        for i in range(20000000):
            total += i * i

        return {
            "status": "success",
            "message": "CPU chaos completed"
        }

@app.route("/chaos/memory")
def chaos_memory():

    REQUEST_COUNT.labels(
        method="GET",
        endpoint="/chaos/memory"
    ).inc()

    with REQUEST_LATENCY.labels(
        method="GET",
        endpoint="/chaos/memory"
    ).time():

        memory_hog = []

        for _ in range(15):
            memory_hog.append("A" * 10_000_000)

        time.sleep(2)

        return {
            "status": "success",
            "message": "Memory chaos injected"
        }

@app.route("/chaos")
def chaos():
    return render_template("chaos.html")

@app.route("/history")
def history():

    history_dir = "/app/test_history"

    os.makedirs(history_dir, exist_ok=True)

    files = sorted(
        os.listdir(history_dir),
        reverse=True
    )

    history_data = []

    for filename in files:

        if filename.endswith(".json"):

            filepath = os.path.join(
                history_dir,
                filename
            )

            with open(filepath, "r") as file:

                data = json.load(file)

                history_data.append({
                    "file": filename,
                    "results": data.get("results", {}),
                    "incidents": data.get("incidents", []),
                    "system_metrics": data.get(
                        "system_metrics",
                        {}
                    )
                })

    return jsonify(history_data)

@app.route("/history-dashboard")
def history_dashboard():
    return render_template("history.html")

@app.route("/compare")
def compare_tests():

    history_dir = "/app/test_history"

    files = sorted(
        [
            file for file in os.listdir(history_dir)
            if file.endswith(".json")
        ],
        reverse=True
    )

    if len(files) < 2:

        return {
            "status": "failure",
            "message": "At least two tests required"
        }

    latest_file = files[0]
    previous_file = files[1]

    with open(
        os.path.join(history_dir, latest_file),
        "r"
    ) as file:

        latest = json.load(file)

    with open(
        os.path.join(history_dir, previous_file),
        "r"
    ) as file:

        previous = json.load(file)

    latest_results = latest["results"]
    previous_results = previous["results"]

    comparison = {

        "latest_test": latest_file,
        "previous_test": previous_file,

        "latency_change_percent":

            round(
                (
                    (
                        latest_results[
                            "average_latency_ms"
                        ]
                        -
                        previous_results[
                            "average_latency_ms"
                        ]
                    )
                    /
                    previous_results[
                        "average_latency_ms"
                    ]
                ) * 100,
                2
            ),

        "throughput_change_percent":

            round(
                (
                    (
                        latest_results[
                            "throughput_rps"
                        ]
                        -
                        previous_results[
                            "throughput_rps"
                        ]
                    )
                    /
                    previous_results[
                        "throughput_rps"
                    ]
                ) * 100,
                2
            ),

        "error_change_percent":

            round(
                (
                    (
                        latest_results[
                            "error_percentage"
                        ]
                        -
                        previous_results[
                            "error_percentage"
                        ]
                    )
                    /
                    (
                        previous_results[
                            "error_percentage"
                        ] or 1
                    )
                ) * 100,
                2
            )
    }

    return comparison

@app.route("/compare-dashboard")
def compare_dashboard():
    return render_template("compare.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)