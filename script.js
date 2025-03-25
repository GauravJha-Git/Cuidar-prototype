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




// //  hospitals
// let hospitalsData = [];
// let hospitalsIndex = 0;

// // Function to get user location
// function hospitalsGetUserLocation() {
//     if (navigator.geolocation) {
//         navigator.geolocation.getCurrentPosition(hospitalsSuccess, hospitalsError);
//     } else {
//         hospitalsShowError();
//     }
// }

// // If location is granted
// function hospitalsSuccess(position) {
//     let lat = position.coords.latitude;
//     let lng = position.coords.longitude;
//     hospitalsFetchNearby(lat, lng);
// }

// // If location is denied
// function hospitalsError() {
//     document.getElementById("hospitals-location-error").classList.remove("hospitals-hidden");
//     document.querySelector(".hospitals-container").classList.add("hospitals-hidden");
// }

// // Fetch hospitals from Overpass API
// function hospitalsFetchNearby(lat, lng) {
//     let url = `https://overpass-api.de/api/interpreter?data=[out:json];node[amenity=hospital](around:5000,${lat},${lng});out;`;

//     fetch(url)
//         .then(response => response.json())
//         .then(data => {
//             if (data.elements.length > 0) {
//                 hospitalsData = data.elements;
//                 hospitalsDisplay();
//             } else {
//                 hospitalsShowError("No hospitals found nearby.");
//             }
//         })
//         .catch(() => hospitalsShowError("Error fetching hospital data."));
// }

// // Show error message if location is not granted
// function hospitalsShowError(message = "Location access is required.") {
//     document.getElementById("hospitals-location-error").classList.remove("hospitals-hidden");
//     document.querySelector(".hospitals-container").classList.add("hospitals-hidden");
//     document.getElementById("hospitals-location-error").innerHTML = `<p>${message}</p><button onclick="hospitalsGetUserLocation()">Grant Location</button>`;
// }

// // Display hospitals in the list
// function hospitalsDisplay() {
//     const container = document.getElementById("hospitals-list");
//     container.innerHTML = "";

//     hospitalsData.forEach(hospital => {
//         let name = hospital.tags.name || "Unknown Hospital";
//         let address = hospital.tags["addr:full"] || "Address not available";
//         let phone = hospital.tags["contact:phone"] ? `<a href="tel:${hospital.tags["contact:phone"]}">📞 Call</a>` : "";

//         let card = `
//             <div class="hospitals-card">
//                 <h3>${name}</h3>
//                 <p>${address}</p>
//                 ${phone}
//             </div>
//         `;
//         container.innerHTML += card;
//     });

//     document.getElementById("hospitals-location-error").classList.add("hospitals-hidden");
//     document.querySelector(".hospitals-container").classList.remove("hospitals-hidden");
// }

// // Scroll hospitals list
// function hospitalsScroll(direction) {
//     const container = document.getElementById("hospitals-list");
//     const cardWidth = 270; // Card width + margin
//     hospitalsIndex += direction;

//     if (hospitalsIndex < 0) hospitalsIndex = 0;
//     if (hospitalsIndex > hospitalsData.length - 1) hospitalsIndex = hospitalsData.length - 1;

//     container.style.transform = `translateX(${-hospitalsIndex * cardWidth}px)`;
// }

// // Call location function when page loads
// hospitalsGetUserLocation();


// //hospitals end

// //emergency
// async function fetchNearestHospital() {
//   if ("geolocation" in navigator) {
//       navigator.geolocation.getCurrentPosition(async (position) => {
//           let lat = position.coords.latitude;
//           let lon = position.coords.longitude;
          
//           let url = `https://nominatim.openstreetmap.org/search?format=json&q=hospital+near+${lat},${lon}`;
          
//           let response = await fetch(url);
//           let data = await response.json();

//           if (data.length > 0) {
//               document.getElementById("hospital-name").innerText = data[0].display_name.split(",")[0];
//               document.getElementById("hospital-address").innerText = data[0].display_name;
//           } else {
//               document.getElementById("hospital-name").innerText = "No hospital found nearby.";
//               document.getElementById("hospital-address").innerText = "";
//           }
//       });
//   } else {
//       document.getElementById("hospital-name").innerText = "Geolocation not supported.";
//   }
// }

// fetchNearestHospital();


// function showPopup() {
//   let popup = document.getElementById("popup");
//   popup.style.display = "flex";

//   setTimeout(() => {
//       popup.style.display = "none";
//   }, 5000);
// }

// document.getElementById("call-ambulance").addEventListener("click", showPopup);
// document.getElementById("call-doctor").addEventListener("click", showPopup);

// document.getElementById("close-popup").addEventListener("click", () => {
//   document.getElementById("popup").style.display = "none";
// });


// hospitals
let hospitalsData = [];
let hospitalsIndex = 0;

// Function to get user location
function hospitalsGetUserLocation() {
    if (navigator.geolocation) {
        document.getElementById("hospitals-loading").classList.remove("hospitals-hidden");
        navigator.geolocation.getCurrentPosition(hospitalsSuccess, hospitalsError);
    } else {
        hospitalsShowError();
    }
}

// If location is granted
function hospitalsSuccess(position) {
    let lat = position.coords.latitude;
    let lng = position.coords.longitude;
    hospitalsFetchNearby(lat, lng);
}

// If location is denied
function hospitalsError() {
    document.getElementById("hospitals-location-error").classList.remove("hospitals-hidden");
    document.querySelector(".hospitals-container").classList.add("hospitals-hidden");
    document.getElementById("hospitals-loading").classList.add("hospitals-hidden");
}

// Fetch hospitals from Overpass API
function hospitalsFetchNearby(lat, lng) {
    let url = `https://overpass-api.de/api/interpreter?data=[out:json];node[amenity=hospital](around:5000,${lat},${lng});out;`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            document.getElementById("hospitals-loading").classList.add("hospitals-hidden");

            if (data.elements.length > 0) {
                hospitalsData = data.elements;
                hospitalsDisplay();
            } else {
                hospitalsShowError("No hospitals found nearby.");
            }
        })
        .catch(() => {
            document.getElementById("hospitals-loading").classList.add("hospitals-hidden");
            hospitalsShowError("Error fetching hospital data.");
        });
}

// Show error message if location is not granted
function hospitalsShowError(message = "Location access is required.") {
    document.getElementById("hospitals-location-error").classList.remove("hospitals-hidden");
    document.querySelector(".hospitals-container").classList.add("hospitals-hidden");
    document.getElementById("hospitals-location-error").innerHTML = `<p>${message}</p><button onclick="hospitalsGetUserLocation()">Grant Location</button>`;
}

// Display hospitals in the list
function hospitalsDisplay() {
    const container = document.getElementById("hospitals-list");
    container.innerHTML = "";

    hospitalsData.forEach(hospital => {
        let name = hospital.tags.name || "Unknown Hospital";
        let address = hospital.tags["addr:full"] || "Address not available";
        let phone = hospital.tags["contact:phone"] ? `<a href="tel:${hospital.tags["contact:phone"]}">📞 Call</a>` : "";

        let card = `
            <div class="hospitals-card">
                <h3>${name}</h3>
                <p>${address}</p>
                ${phone}
            </div>
        `;
        container.innerHTML += card;
    });

    document.getElementById("hospitals-location-error").classList.add("hospitals-hidden");
    document.querySelector(".hospitals-container").classList.remove("hospitals-hidden");
}

// Scroll hospitals list
function hospitalsScroll(direction) {
    const container = document.getElementById("hospitals-list");
    const cardWidth = 270; // Card width + margin
    hospitalsIndex += direction;

    if (hospitalsIndex < 0) hospitalsIndex = 0;
    if (hospitalsIndex > hospitalsData.length - 1) hospitalsIndex = hospitalsData.length - 1;

    container.style.transform = `translateX(${-hospitalsIndex * cardWidth}px)`;
}

// Call location function when page loads
hospitalsGetUserLocation();


// emergency
async function fetchNearestHospital() {
    if ("geolocation" in navigator) {
        document.getElementById("emergency-loading").classList.remove("hospitals-hidden");

        navigator.geolocation.getCurrentPosition(async (position) => {
            let lat = position.coords.latitude;
            let lon = position.coords.longitude;

            let url = `https://nominatim.openstreetmap.org/search?format=json&q=hospital+near+${lat},${lon}`;

            let response = await fetch(url);
            let data = await response.json();

            document.getElementById("emergency-loading").classList.add("hospitals-hidden");
            document.getElementById("hospital-name").classList.remove("hospitals-hidden");
            document.getElementById("hospital-address").classList.remove("hospitals-hidden");

            if (data.length > 0) {
                document.getElementById("hospital-name").innerText = data[0].display_name.split(",")[0];
                document.getElementById("hospital-address").innerText = data[0].display_name;
            } else {
                document.getElementById("hospital-name").innerText = "No hospital found nearby.";
                document.getElementById("hospital-address").innerText = "";
            }
        });
    } else {
        document.getElementById("hospital-name").innerText = "Geolocation not supported.";
    }
}

fetchNearestHospital();

function showPopup() {
    let popup = document.getElementById("popup");
    popup.style.display = "flex";

    setTimeout(() => {
        popup.style.display = "none";
    }, 5000);
}

document.getElementById("call-ambulance").addEventListener("click", showPopup);
document.getElementById("call-doctor").addEventListener("click", showPopup);
document.getElementById("close-popup").addEventListener("click", () => {
    document.getElementById("popup").style.display = "none";
});
