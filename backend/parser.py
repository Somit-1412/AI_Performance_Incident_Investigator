import csv


def parse_jmeter_results(file_path):

    total_requests = 0
    failed_requests = 0

    response_times = []

    with open(file_path, newline='') as csvfile:

        reader = csv.DictReader(csvfile)

        for row in reader:

            total_requests += 1

            elapsed = int(row["elapsed"])
            response_times.append(elapsed)

            success = row["success"]

            if success == "false":
                failed_requests += 1

    average_latency = (
        sum(response_times) / len(response_times)
        if response_times else 0
    )

    max_latency = max(response_times) if response_times else 0

    min_latency = min(response_times) if response_times else 0

    error_percentage = (
        (failed_requests / total_requests) * 100
        if total_requests > 0 else 0
    )

    return {
        "total_requests": total_requests,
        "failed_requests": failed_requests,
        "average_latency_ms": round(average_latency, 2),
        "max_latency_ms": max_latency,
        "min_latency_ms": min_latency,
        "error_percentage": round(error_percentage, 2)
    }