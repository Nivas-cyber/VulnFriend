// Simulate terminal typing effect
document.addEventListener('DOMContentLoaded', function() {
    // Get client IP (simulated)
    fetch('https://api.ipify.org?format=json')
        .then(response => response.json())
        .then(data => {
            document.getElementById('client-ip').textContent = data.ip;
        });
    
    // Add glitch effect to title
    const title = document.querySelector('.title');
    setInterval(() => {
        if (Math.random() > 0.9) {
            title.style.textShadow = '0 0 10px #00ff00';
            setTimeout(() => {
                title.style.textShadow = 'none';
            }, 100);
        }
    }, 1000);
    
    // Easter egg: Konami code
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 
                       'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 
                       'b', 'a'];
    let konamiIndex = 0;
    
    document.addEventListener('keydown', (e) => {
        if (e.key === konamiCode[konamiIndex]) {
            konamiIndex++;
            if (konamiIndex === konamiCode.length) {
                document.body.style.background = 'linear-gradient(45deg, #ff00ff, #00ffff)';
                setTimeout(() => {
                    document.body.style.background = '';
                }, 3000);
                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }
    });
    
    // Add scanlines effect
    const scanlines = document.createElement('div');
    scanlines.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            to bottom,
            transparent 50%,
            rgba(0, 255, 0, 0.03) 50%
        );
        background-size: 100% 4px;
        pointer-events: none;
        z-index: 9999;
    `;
    document.body.appendChild(scanlines);
});