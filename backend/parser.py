import csv
import statistics
from urllib.parse import urlparse

def percentile(data, percentile_value):

    if not data:
        return 0

    data = sorted(data)

    index = int((percentile_value / 100) * len(data)) - 1

    index = max(0, index)

    return data[index]

def parse_jmeter_results(file_path):

    total_requests = 0
    failed_requests = 0

    response_times = []
    timestamps = []

    endpoint_metrics = {}

    with open(file_path, newline='') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            total_requests += 1

            elapsed = int(row["elapsed"])

            response_times.append(elapsed)

            timestamps.append(int(row["timeStamp"]))

            success = row["success"]

            label = urlparse(row["URL"]).path

            if success == "false":
                failed_requests += 1

            if label not in endpoint_metrics:

                endpoint_metrics[label] = {
                    "count": 0,
                    "errors": 0,
                    "latencies": []
                }

            endpoint_metrics[label]["count"] += 1

            endpoint_metrics[label]["latencies"].append(elapsed)

            if success == "false":
                endpoint_metrics[label]["errors"] += 1

    average_latency = (
        sum(response_times) / len(response_times)
        if response_times else 0
    )

    max_latency = max(response_times) if response_times else 0

    min_latency = min(response_times) if response_times else 0

    p95_latency = percentile(response_times, 95)

    p99_latency = percentile(response_times, 99)

    test_duration_seconds = (
    (max(timestamps) - min(timestamps)) / 1000
    if timestamps else 1
    )

    throughput = total_requests / test_duration_seconds

    error_percentage = (
        (failed_requests / total_requests) * 100
        if total_requests > 0 else 0
    )

    endpoint_summary = {}

    for endpoint, data in endpoint_metrics.items():

        avg_latency = (
            sum(data["latencies"]) / len(data["latencies"])
        )

        endpoint_error_percentage = (
            data["errors"] / data["count"]
        ) * 100

        endpoint_summary[endpoint] = {

            "requests": data["count"],

            "avg_latency_ms": round(avg_latency, 2),

            "error_percentage": round(
                endpoint_error_percentage,
                2
            )
        }

    return {
        "total_requests": total_requests,
        "failed_requests": failed_requests,
        "average_latency_ms": round(average_latency, 2),
        "max_latency_ms": max_latency,
        "min_latency_ms": min_latency,
        "p95_latency_ms": p95_latency,
        "p99_latency_ms": p99_latency,
        "throughput_rps": round(throughput, 2),
        "error_percentage": round(error_percentage, 2),
        "endpoint_metrics": endpoint_summary
    }