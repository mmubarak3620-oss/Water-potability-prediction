document.getElementById("predictionForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const data = {
        ph: document.getElementById("ph").value,
        hardness: document.getElementById("hardness").value,
        solids: document.getElementById("solids").value,
        chloramines: document.getElementById("chloramines").value,
        sulfate: document.getElementById("sulfate").value,
        conductivity: document.getElementById("conductivity").value,
        organic_carbon: document.getElementById("organic_carbon").value,
        trihalomethanes: document.getElementById("trihalomethanes").value,
        turbidity: document.getElementById("turbidity").value
    };

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        console.log("Backend response:", result);
      document.getElementById("result").innerText = result.prediction;
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Backend connection error");
    });
});