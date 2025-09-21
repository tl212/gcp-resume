document.addEventListener('DOMContentLoaded', function() {
    // fetch the visitor count from the backend
    fetch('https://visitor-counter-uasgf6ueta-uc.a.run.app', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // update the visitor counter element with retro formatting
            const visitorCountElement = document.getElementById('visitorCount');
            if (visitorCountElement) {
                // format the count with leading zeros for retro look
                const formattedCount = data.count.toString().padStart(5, '0');
                visitorCountElement.textContent = formattedCount;
            }
        })
        .catch(error => {
            console.error('Error fetching visitor count:', error);
            // fallback display if backend fails
            const visitorCountElement = document.getElementById('visitorCount');
            if (visitorCountElement) {
                visitorCountElement.textContent = '-----';
            }
        });
});
