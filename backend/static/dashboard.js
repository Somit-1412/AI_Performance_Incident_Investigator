async function loadDashboard() {

    const dashboardContent =
        document.getElementById("dashboard-content");

    try {

        const response =
            await fetch("/latest-result");

        const data = await response.json();

        dashboardContent.innerHTML = `

        <div class="card bg-secondary text-light mb-4">
            <div class="card-body">

                <h3 class="card-title mb-4">
                    Performance Metrics
                </h3>

                <div class="row">

                    <div class="col-md-4 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>Average Latency</h5>
                                <p>${data.results.average_latency_ms} ms</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>P95 Latency</h5>
                                <p>${data.results.p95_latency_ms} ms</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>P99 Latency</h5>
                                <p>${data.results.p99_latency_ms} ms</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>Throughput</h5>
                                <p>${data.results.throughput_rps} req/sec</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>Error Percentage</h5>
                                <p>${data.results.error_percentage}%</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-4 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>Total Requests</h5>
                                <p>${data.results.total_requests}</p>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
        </div>

        <div class="card bg-secondary text-light mb-4">
            <div class="card-body">

                <h3 class="card-title mb-4">
                    System Metrics
                </h3>

                <div class="row">

                    <div class="col-md-6 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>CPU Usage</h5>
                                <p>${data.system_metrics.cpu_usage_percent}%</p>
                            </div>
                        </div>
                    </div>

                    <div class="col-md-6 mb-3">
                        <div class="card bg-dark text-light">
                            <div class="card-body">
                                <h5>Memory Usage</h5>
                                <p>${data.system_metrics.memory_usage_percent}%</p>
                            </div>
                        </div>
                    </div>

                </div>

            </div>
        </div>

        <div class="card bg-secondary text-light mb-4">
            <div class="card-body">

                <h3 class="card-title mb-4">
                    Detected Incidents
                </h3>

                ${
                    data.incidents.map(incident => `

                        <div class="alert ${
                            incident.severity === "critical"
                                ? "alert-danger"
                                : incident.severity === "warning"
                                ? "alert-warning"
                                : "alert-success"
                        }">

                            <strong>${incident.type}</strong>

                            <br>

                            ${incident.message}

                        </div>

                    `).join("")
                }

            </div>
        </div>

        <div class="card bg-secondary text-light mb-4">
            <div class="card-body">

                <h3 class="card-title mb-4">
                    AI Root Cause Analysis
                </h3>

                <div>
                    ${marked.parse(data.ai_analysis)}
                </div>

            </div>
        </div>

        `;

    } catch (error) {

        dashboardContent.innerHTML = `

            <div class="alert alert-danger">
                Failed to load dashboard data
            </div>

        `;
    }
}

loadDashboard();