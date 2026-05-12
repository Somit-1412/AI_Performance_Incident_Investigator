def analyze_incident(results, test_context):

    incidents = []

    error_percentage = results["error_percentage"]
    p95_latency = results["p95_latency_ms"]
    throughput = results["throughput_rps"]
    users = int(test_context["users"])

    if error_percentage > 10:
        incidents.append({
            "severity": "critical",
            "type": "High Error Rate",
            "message": f"Error rate reached {error_percentage}%"
        })

    if p95_latency > 1000:
        incidents.append({
            "severity": "warning",
            "type": "High Latency",
            "message": f"P95 latency is {p95_latency} ms"
        })

    if users > 50 and throughput < (users * 0.5):
        incidents.append({
            "severity": "warning",
            "type": "Low Throughput",
            "message": f"Throughput dropped to {throughput} requests/sec"
        })

    if not incidents:
        incidents.append({
            "severity": "info",
            "type": "Healthy System",
            "message": "No major incidents detected"
        })

    return incidents