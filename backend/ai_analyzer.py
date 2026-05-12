from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def build_analysis_prompt(results, incidents, system_metrics, test_context):
    prompt = f"""
You are an AI performance investigation assistant.

Only use the provided metrics, incidents, and test context.

Do NOT assume:
- database systems
- caches
- external APIs
- network failures
- infrastructure bottlenecks
unless explicitly supported by metrics.

Base conclusions strictly on:
- latency
- throughput
- error percentage
- CPU usage
- memory usage
- incident data
- target endpoint behavior

If evidence is insufficient, explicitly say:
"Root cause cannot be determined conclusively from available metrics."

Analyze the following load test results.

Load Test Metrics:
- Total Requests: {results['total_requests']}
- Failed Requests: {results['failed_requests']}
- Error Percentage: {results['error_percentage']}%
- Average Latency: {results['average_latency_ms']} ms
- P95 Latency: {results['p95_latency_ms']} ms
- P99 Latency: {results['p99_latency_ms']} ms
- Throughput: {results['throughput_rps']} requests/sec

System Metrics:
- CPU Usage: {system_metrics['cpu_usage_percent']}%
- Memory Usage: {system_metrics['memory_usage_percent']}%

Test Context:
- Target Endpoint: {test_context['path']}
- Virtual Users: {test_context['users']}
- Ramp-Up: {test_context['rampup']} seconds
- Loop Count: {test_context['loops']}
- Think Time: {test_context['timer']} ms

Detected Incidents:
"""

    for incident in incidents:
        prompt += f"""
- Severity: {incident['severity']}
  Type: {incident['type']}
  Message: {incident['message']}
"""

    prompt += """

If system appears healthy, state that clearly.

Return:
1. System health summary
2. Performance observations
3. Incident impact
4. Recommendations strictly supported by metrics
"""

    return prompt

def generate_ai_analysis(results, incidents, system_metrics, test_context):

    prompt = build_analysis_prompt(
        results,
        incidents,
        system_metrics,
        test_context
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": "You are an expert performance engineer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content