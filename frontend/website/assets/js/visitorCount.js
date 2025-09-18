// visitorCount();

// async function visitorCount() {
//     try {
//         const response = await fetch('https://backend-msvsj56xlq-uk.a.run.app/count');
//         const data = await response.json();
//         console.log(data);
//         document.getElementById('count').innerHTML = data.count;
//     } catch (error) {
//         console.error(error);
//     }
// }


document.addEventListener('DOMContentLoaded', function() {
    // Assuming you're fetching the visitor count from your backend
    fetch('https://app-msvsj56xlq-uk.a.run.app/count', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            const visitorCountElement = document.querySelector('.visitorCounter');
            if (visitorCountElement) {
                visitorCountElement.innerHTML = data.count;
            }
        })
        .catch(error => console.error('Error:', error));
});
