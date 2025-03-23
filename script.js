document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('backgroundCanvas');
    const ctx = canvas.getContext('2d');
    let animationFrameId;
    let particles = [];
    
    // Create medical cross path
    function createCrossPath(ctx, x, y, size) {
      const third = size / 3;
      ctx.beginPath();
      ctx.moveTo(x - third, y - third * 3);
      ctx.lineTo(x + third, y - third * 3);
      ctx.lineTo(x + third, y - third);
      ctx.lineTo(x + third * 3, y - third);
      ctx.lineTo(x + third * 3, y + third);
      ctx.lineTo(x + third, y + third);
      ctx.lineTo(x + third, y + third * 3);
      ctx.lineTo(x - third, y + third * 3);
      ctx.lineTo(x - third, y + third);
      ctx.lineTo(x - third * 3, y + third);
      ctx.lineTo(x - third * 3, y - third);
      ctx.lineTo(x - third, y - third);
      ctx.closePath();
    }
    
    // Initialize particles
    function initParticles() {
      particles = [];
      const particleCount = Math.floor(canvas.width * canvas.height / 20000);
      
      for (let i = 0; i < particleCount; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 12 + 8,
          speedX: (Math.random() - 0.5) * 0.8,
          speedY: (Math.random() - 0.5) * 0.8,
          opacity: Math.random() * 0.3 + 0.1,
          rotation: Math.random() * Math.PI * 2,
          rotationSpeed: (Math.random() - 0.5) * 0.02
        });
      }
    }
    
    // Set canvas dimensions
    function handleResize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      initParticles();
    }
    
    // Setup event listeners
    window.addEventListener('resize', handleResize);
    handleResize();
    
    // Draw function
    function draw() {
      // Clear canvas
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      
      // Draw background
      ctx.fillStyle = '#f8fcf8';
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      
      // Draw particles
      for (let i = 0; i < particles.length; i++) {
        const p = particles[i];
        
        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate(p.rotation);
        
        // Draw medical cross
        ctx.fillStyle = `rgba(128, 249, 150, ${p.opacity})`;
        createCrossPath(ctx, 0, 0, p.size);
        ctx.fill();
        
        ctx.restore();
        
        // Update position
        p.x += p.speedX;
        p.y += p.speedY;
        p.rotation += p.rotationSpeed;
        
        // Wrap around
        if (p.x < -p.size) p.x = canvas.width + p.size;
        if (p.x > canvas.width + p.size) p.x = -p.size;
        if (p.y < -p.size) p.y = canvas.height + p.size;
        if (p.y > canvas.height + p.size) p.y = -p.size;
      }
      
      // Draw connecting lines
      ctx.strokeStyle = 'rgba(128, 249, 150, 0.15)';
      ctx.lineWidth = 1;
      
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const distance = Math.sqrt(dx * dx + dy * dy);
          
          if (distance < 150) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.stroke();
          }
        }
      }
      
      animationFrameId = window.requestAnimationFrame(draw);
    }
    
    // Start animation
    draw();
    
    // Cleanup on page unload
    window.addEventListener('unload', function() {
      window.cancelAnimationFrame(animationFrameId);
      window.removeEventListener('resize', handleResize);
    });
  });