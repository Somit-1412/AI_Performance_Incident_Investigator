async function startTest() {

    const baseUrl =document.getElementById("baseUrl").value || "http://localhost:5000";
    const path = document.getElementById("path").value || "/fast";
    const journeyEndpoints =
        document.getElementById("journeyEndpoints").value;
    const users = document.getElementById("users").value || "50";
    const rampup = document.getElementById("rampup").value || "5";
    const loops =   document.getElementById("loops").value || "5";
    const timer =
        document.getElementById("timer").value || "500";
    const executionMode =
        document.getElementById(
            "execution_mode"
        ).value;
    const chaosTypes = [];

        if (
            document.getElementById(
                "chaos_latency"
            ).checked
        ) {
            chaosTypes.push("latency");
        }

        if (
            document.getElementById(
                "chaos_failure"
            ).checked
        ) {
            chaosTypes.push("failure");
        }

        if (
            document.getElementById(
                "chaos_cpu"
            ).checked
        ) {
            chaosTypes.push("cpu");
        }

        if (
            document.getElementById(
                "chaos_memory"
            ).checked
        ) {
            chaosTypes.push("memory");
        }
    const startButton = 
        document.getElementById("startButton");

    try {
        startButton.disabled = true;

        startButton.innerText =
            "Running Test...";

        const response = await fetch(
            `http://localhost:5000/start-test?baseUrl=${encodeURIComponent(baseUrl)}&path=${encodeURIComponent(path)}&users=${users}&rampup=${rampup}&loops=${loops}&timer=${timer}&journeyEndpoints=${encodeURIComponent(journeyEndpoints)}&execution_mode=${executionMode}&chaos_types=${chaosTypes.join(",")}`
        );

        await response.json();

        window.location.href = "/dashboard";

    } catch (error) {
        startButton.disabled = false;

        startButton.innerText =
            "Start Test";

        alert("Error running test");
    }
}