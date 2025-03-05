async function updateLED(ledId, state) {
    let response = await fetch('/led/' + ledId, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({state: state})
    });
    let result = await response.json();
    document.getElementById("status" + ledId).innerText = "LED " + ledId + " is " + (state ? "ON" : "OFF");

    // Toggle the icons based on the state
    const ledIconOn = document.getElementById("led-icon-on" + ledId);

    if (state) {
        ledIconOn.style.display = 'block';  // Show LED icon when ON
    } else {
        ledIconOn.style.display = 'none';   // Hide LED icon when OFF
    }

    // Removed the status-update message
}

async function getLEDStates() {
    for (let i = 1; i <= 3; i++) {
        let response = await fetch('/led/' + i);
        if (response.ok) {
            let data = await response.json();
            const ledElement = document.getElementById("led-switch" + i);
            const ledIconOn = document.getElementById("led-icon-on" + i);

            if (data.state) {
                ledElement.classList.add('on');
                ledIconOn.style.display = 'block';  // Show LED icon when ON
            } else {
                ledElement.classList.remove('on');
                ledIconOn.style.display = 'none';  // Hide LED icon when OFF
            }
            document.getElementById("status" + i).innerText = "LED " + i + " is " + (data.state ? "ON" : "OFF");
        } else {
            console.error("Failed to fetch LED " + i + " state.");
        }
    }
}

setInterval(getLEDStates, 1000);  // Fetch LED states every 1 second
