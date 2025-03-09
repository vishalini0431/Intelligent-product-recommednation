document.addEventListener("DOMContentLoaded", function () {
    // Handle click on Settings link to open the modal
    document.getElementById('settingsLink').addEventListener('click', function () {
        $('#settingsModal').modal('show');
    });

    // Theme change functionality
    document.getElementById('applyTheme').addEventListener('click', function () {
        let selectedTheme = document.querySelector('input[name="theme"]:checked').value;
        if (selectedTheme === "black") {
            document.body.style.backgroundColor = "#000";
            document.body.style.color = "#fff";
        } else if (selectedTheme === "green") {
            document.body.style.backgroundColor = "#28a745";
            document.body.style.color = "#fff";
        } else {
            document.body.style.backgroundColor = "#f8f9fa";
            document.body.style.color = "#000";
        }
    });

    // Zoom functionality
    let zoomLevel = 1;
    document.getElementById('zoomIn').addEventListener('click', function () {
        zoomLevel += 0.1;
        document.body.style.zoom = zoomLevel;
    });

    document.getElementById('zoomOut').addEventListener('click', function () {
        if (zoomLevel > 0.5) {
            zoomLevel -= 0.1;
            document.body.style.zoom = zoomLevel;
        }
    });
});
