function findRoute() {
    const start = document.getElementById("start").value;
    const end = document.getElementById("end").value;
    const ecoMode = document.getElementById("mode").value;

    const results = document.getElementById("results");
    results.innerHTML = "Calculating route…";

    fetch("http://127.0.0.1:5000/route", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            start: start,
            end: end,
            eco_mode: ecoMode
        })
    })
    .then(r => r.json())
    .then(data => {
        if (data.status !== "success") {
            results.innerHTML = `<p style="color:red;">${data.message}</p>`;
            return;
        }

        const r = data.data;

        results.innerHTML = `
            <h3>Route Found!</h3>
            <p><strong>Route:</strong> ${r.description}</p>
            <p><strong>Distance:</strong> ${r.distance_km} km</p>
            <p><strong>CO2 Saved:</strong> ${r.co2_saved} kg</p>
            <p><strong>Points Earned:</strong> ${r.points}</p>
        `;
    })
    .catch(err => {
        results.innerHTML = `<p style="color:red;">Server error: ${err}</p>`;
    });
}
