# AI Performance Incident Investigator

An AI-powered performance engineering and chaos testing platform that combines load testing, observability, historical trend analysis, regression comparison, and AI-generated root cause analysis.

The platform allows users to:
- Conduct load tests on real-world websites
- Inject chaos scenarios
- Monitor system performance
- Analyze incidents using AI
- Compare historical test runs
- Visualize trends and regressions

---

# Features

## Load Testing
- Apache JMeter integration
- Dynamic external website testing
- Customer journey simulation
- Configurable:
  - Virtual users
  - Ramp-up time
  - Loop count
  - Think time

---

## Chaos Engineering

Supported chaos types:
- Latency chaos
- Failure chaos
- CPU stress
- Memory stress

Execution modes:
- Load Test Only
- Chaos Only
- Load + Chaos

Chaos runs concurrently with load testing.

---

# AI Incident Analysis

AI-generated:
- Root cause analysis
- Performance degradation analysis
- Incident interpretation
- Recommendations
- Comparative regression analysis

Powered using Groq LLM integration.

---

# Observability Stack

Integrated monitoring using:
- Prometheus
- Grafana
- Node Exporter

Metrics monitored:
- CPU usage
- Memory usage
- Average latency
- P95 latency
- Throughput
- Error percentage

---

# Historical Analysis

Stores all test executions as JSON history.

Supports:
- Historical result tracking
- Trend visualization
- Regression comparison
- AI comparative analysis

---

# Tech Stack

## Backend
- Python
- Flask

## Performance Testing
- Apache JMeter

## Monitoring
- Prometheus
- Grafana
- Node Exporter

## AI
- Groq API
- LLM-based analysis

## Infrastructure
- Docker
- Docker Compose

---

# System Architecture

```text
User
  ↓
Flask Web UI
  ↓
JMeter Load Execution
  ↓
Target Website

Simultaneously:
- Chaos Injection Engine
- Prometheus Monitoring
- Grafana Visualization
- AI Analysis Engine