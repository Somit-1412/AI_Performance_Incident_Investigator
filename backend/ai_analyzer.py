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
- endpoint-specific metrics
- target endpoint behavior

Use endpoint metrics to identify:
- which endpoint is causing latency
- which endpoint is causing failures
- which endpoints are healthy

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
- Primary Endpoint: {test_context['path']}
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
        
    prompt += f"""

Endpoint Metrics:
{results.get('endpoint_metrics', {})}
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

def generate_comparison_analysis(comparison):

    prompt = f"""
You are a performance engineering analyst.

Analyze the following comparison results
between two performance test executions.

Comparison Metrics:

- Latency Change:
  {comparison['latency_change_percent']}%

- Throughput Change:
  {comparison['throughput_change_percent']}%

- Error Rate Change:
  {comparison['error_change_percent']}%

Interpretation Rules:

- Positive latency change means performance degradation.
- Negative latency change means performance improvement.

- Positive error rate change means worse stability.
- Negative error rate change means improved stability.

- Positive throughput change means better capacity.
- Negative throughput change means degraded capacity.

Rules:

- If latency change is positive,
  explicitly state latency degradation.

- If error rate change is negative,
  explicitly state stability improvement.

- Do not contradict metric semantics.

- Do not claim overall improvement
  if latency degradation is significant.

- Base conclusions strictly on metric signs.
  
Explain:

1. Whether performance improved or degraded
2. Whether system stability improved or degraded
3. Possible operational impact

Keep analysis concise and evidence-based.
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {
                "role": "system",
                "content":
                "You are an expert performance engineer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        temperature=0.3
    )

    return response.choices[0].message.content