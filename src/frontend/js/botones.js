// Adding buttons for Phase 1 and Phase 2 functionality

document.addEventListener('DOMContentLoaded', () => {
    // Create button for Phase 1
    const phase1Button = document.createElement('button');
    phase1Button.textContent = 'Go to Phase 1';
    phase1Button.id = 'phase1Button';
    phase1Button.addEventListener('click', () => {
        alert('Navigating to Phase 1...');
        // Logic to switch to Phase 1 goes here
        window.location.href = '/phase1'; // Example navigation
    });
    
    // Create button for Phase 2
    const phase2Button = document.createElement('button');
    phase2Button.textContent = 'Go to Phase 2';
    phase2Button.id = 'phase2Button';
    phase2Button.addEventListener('click', () => {
        alert('Navigating to Phase 2...');
        // Logic to switch to Phase 2 goes here
        window.location.href = '/phase2'; // Example navigation
    });
    
    // Append buttons to the body or a specific container
    const container = document.getElementById('buttonContainer') || document.body;
    container.appendChild(phase1Button);
    container.appendChild(phase2Button);
});
