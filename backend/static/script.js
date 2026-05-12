async function startTest() {

    const baseUrl =document.getElementById("baseUrl").value;
    const path = document.getElementById("path").value;
    const users = document.getElementById("users").value;
    const rampup = document.getElementById("rampup").value;
    const loops =   document.getElementById("loops").value;
    const timer =
        document.getElementById("timer").value;
    const startButton = 
        document.getElementById("startButton");


    try {
        startButton.disabled = true;

        startButton.innerText =
            "Running Test...";

        const response = await fetch(
            `http://localhost:5000/start-test?baseUrl=${encodeURIComponent(baseUrl)}&path=${encodeURIComponent(path)}&users=${users}&rampup=${rampup}&loops=${loops}&timer=${timer}`
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