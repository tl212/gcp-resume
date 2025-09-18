// Temporary visitor counter - will connect to Cloud Function later
document.addEventListener('DOMContentLoaded', function() {
    // For now, just show a placeholder
    updateVisitorCount();
});

async function updateVisitorCount() {
    const countElement = document.getElementById('count');
    
    try {
        // TODO: Replace with your actual Cloud Function URL
        // const response = await fetch('YOUR_CLOUD_FUNCTION_URL');
        // const data = await response.json();
        // countElement.textContent = data.count;
        
        // Temporary: Show random number for testing
        const tempCount = Math.floor(Math.random() * 1000) + 100;
        countElement.textContent = tempCount;
        
        console.log('Visitor counter will be connected to Cloud Function');
    } catch (error) {
        console.error('Error fetching visitor count:', error);
        countElement.textContent = 'Error';
    }
}

// Add some interactivity
document.addEventListener('DOMContentLoaded', function() {
    // Animate skill tags on hover
    const skills = document.querySelectorAll('.skill-tag');
    skills.forEach(skill => {
        skill.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });
        skill.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
    
    // Smooth scroll for any future navigation
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

console.log('Cloud Resume Challenge - JavaScript Loaded');