function sendCommand(cmd) {
    fetch("/api/control", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ cmd: cmd })
    })
    .then(res => res.json())
    .then(data => {
        console.log(data);

        if (data.status === "ok") {
            document.getElementById("status").innerText =
                "Status: " + data.cmd;
        } else {
            document.getElementById("status").innerText =
                "Error: " + data.message;
        }
    })
    .catch(err => {
        console.log(err);
        document.getElementById("status").innerText =
            "Status: error (undefined)";
    });
}