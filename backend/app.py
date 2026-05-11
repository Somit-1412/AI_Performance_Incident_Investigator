from flask import Flask
import time
import random

app = Flask(__name__)


@app.route("/fast")
def fast():
    return {
        "status": "success",
        "message": "Fast endpoint response"
    }


@app.route("/slow")
def slow():
    time.sleep(3)

    return {
        "status": "success",
        "message": "Slow endpoint response"
    }


@app.route("/error")
def error():
    return {
        "status": "failure",
        "message": "Simulated server error"
    }, 500


@app.route("/cpu")
def cpu():

    total = 0

    for i in range(10000000):
        total += i * i

    return {
        "status": "success",
        "message": "CPU intensive task completed"
    }


@app.route("/")
def home():
    return {
        "message": "AI Performance Incident Investigator Backend Running"
    }


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)