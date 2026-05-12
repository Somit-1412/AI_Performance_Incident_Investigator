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
    const startButton = 
        document.getElementById("startButton");

    try {
        startButton.disabled = true;

        startButton.innerText =
            "Running Test...";

        const response = await fetch(
            `http://localhost:5000/start-test?baseUrl=${encodeURIComponent(baseUrl)}&path=${encodeURIComponent(path)}&users=${users}&rampup=${rampup}&loops=${loops}&timer=${timer}&journeyEndpoints=${encodeURIComponent(journeyEndpoints)}`
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