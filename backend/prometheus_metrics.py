import requests


PROMETHEUS_URL = "http://prometheus:9090/api/v1/query"


def query_prometheus(query):

    response = requests.get(
        PROMETHEUS_URL,
        params={"query": query}
    )

    data = response.json()

    results = data["data"]["result"]

    if not results:
        return 0

    return float(results[0]["value"][1])


def get_system_metrics():

    cpu_query = '''
100 - (avg by(instance)
(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)
'''

    memory_query = '''
(node_memory_MemTotal_bytes - node_memory_MemAvailable_bytes)
/
node_memory_MemTotal_bytes
* 100
'''

    cpu_usage = query_prometheus(cpu_query)

    memory_usage = query_prometheus(memory_query)

    return {
        "cpu_usage_percent": round(cpu_usage, 2),
        "memory_usage_percent": round(memory_usage, 2)
    }