from flask import Flask, jsonify
import psutil
import datetime

app = Flask(__name__)

START_TIME = datetime.datetime.now()


# ---------- Liveness Probe ----------
@app.route("/health/live")
def liveness():

    return jsonify({
        "status": "UP"
    })


# ---------- Readiness Probe ----------
@app.route("/health/ready")
def readiness():

    cpu = psutil.cpu_percent()

    if cpu > 90:

        return jsonify({
            "status": "NOT_READY",
            "cpu_usage": cpu
        }), 503

    return jsonify({
        "status": "READY",
        "cpu_usage": cpu
    })


# ---------- Detailed Health ----------
@app.route("/health")
def health():

    uptime = (
        datetime.datetime.now()
        - START_TIME
    ).total_seconds()

    return jsonify({
        "status": "UP",
        "uptime_seconds": uptime,
        "cpu_usage":
            psutil.cpu_percent(),
        "memory_usage":
            psutil.virtual_memory().percent,
        "disk_usage":
            psutil.disk_usage('/').percent
    })


# ---------- Metrics ----------
@app.route("/metrics")
def metrics():

    return jsonify({
        "cpu":
            psutil.cpu_percent(),
        "memory":
            psutil.virtual_memory().percent
    })


if __name__ == "__main__":

    app.run(debug=True)
