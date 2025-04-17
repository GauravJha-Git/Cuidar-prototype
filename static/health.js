document.addEventListener('DOMContentLoaded', () => {
    // Tab navigation
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // Add active class to clicked button
            button.classList.add('active');
            
            // Hide all tab contents
            tabContents.forEach(content => content.classList.add('hidden'));
            
            // Show the selected tab content
            const tabId = button.getAttribute('data-tab');
            document.getElementById(`${tabId}-content`).classList.remove('hidden');
        });
    });

    // ========== SUGAR LEVEL TRACKER ==========
    const fastingSugarInput = document.getElementById('fasting-sugar');
    const postMealSugarInput = document.getElementById('post-meal-sugar');
    const submitSugarBtn = document.getElementById('submit-sugar-btn');
    const sugarErrorMessage = document.getElementById('sugar-error-message');
    const fastingAverage = document.getElementById('fasting-average');
    const postMealAverage = document.getElementById('post-meal-average');
    const averagesSection = document.getElementById('averages-section');
    const clearSugarBtn = document.getElementById('clear-sugar-btn');
    let sugarChart = null;

    // Default empty data for initial chart display
    const emptyAverages = {
        fasting_levels: [],
        post_meal_levels: [],
        timestamps: []
    };

    // Fetch healthy range
    let healthyRange = {
        fasting_min: 70,
        fasting_max: 100,
        post_meal_min: 70,
        post_meal_max: 140
    };

    fetch('/get_healthy_range')
        .then(response => response.json())
        .then(data => {
            healthyRange = data;
            // Initialize empty chart with healthy ranges
            createSugarChart(emptyAverages);
        })
        .catch(error => {
            console.error('Error fetching healthy range:', error);
            // Still initialize chart with default values
            createSugarChart(emptyAverages);
        });

    // Chart configuration for sugar levels
    function createSugarChart(averages) {
        const ctx = document.getElementById('sugar-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (sugarChart) {
            sugarChart.destroy();
            
        }

        // Prepare labels based on actual timestamps or default to Day 1, Day 2, etc.
        let labels = [];
        let fastingData = [];
        let postMealData = [];

        if (averages.timestamps && averages.timestamps.length > 0) {
            labels = averages.timestamps;
            fastingData = averages.fasting_levels;
            postMealData = averages.post_meal_levels;
        } else {
            // Show empty chart with at least some days on x-axis
            labels = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'];
            fastingData = Array(5).fill(null);
            postMealData = Array(5).fill(null);
        }

        sugarChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Fasting Sugar Levels',
                        data: fastingData,
                        borderColor: 'blue',
                        backgroundColor: 'rgba(0, 0, 255, 0.1)',
                        tension: 0.1
                    },
                    {
                        label: 'Post Meal Sugar Levels',
                        data: postMealData,
                        borderColor: 'red',
                        backgroundColor: 'rgba(255, 0, 0, 0.1)',
                        tension: 0.1
                    },
                    {
                        label: 'Healthy Fasting Min',
                        data: Array(labels.length).fill(healthyRange.fasting_min),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Healthy Fasting Max',
                        data: Array(labels.length).fill(healthyRange.fasting_max),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Healthy Post Meal Min',
                        data: Array(labels.length).fill(healthyRange.post_meal_min),
                        borderColor: 'orange',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Healthy Post Meal Max',
                        data: Array(labels.length).fill(healthyRange.post_meal_max),
                        borderColor: 'orange',
                        borderDash: [5, 5],
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Sugar Level Tracking'
                    },
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Sugar Level (mg/dL)'
                        },
                        min: 50,  // Set minimum value to ensure y-axis shows a good range
                        max: 160  // Set maximum to show healthy ranges clearly
                    }
                }
            }
        });
    }

    // Submit sugar levels
    submitSugarBtn.addEventListener('click', () => {
        const fastingSugar = parseFloat(fastingSugarInput.value);
        const postMealSugar = parseFloat(postMealSugarInput.value);

        // Basic validation
        if (isNaN(fastingSugar) || isNaN(postMealSugar)) {
            sugarErrorMessage.textContent = 'Please enter valid sugar levels';
            return;
        }

        // Clear previous error
        sugarErrorMessage.textContent = '';

        // Send data to backend
        fetch('/add_sugar_level', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                fasting_sugar: fastingSugar,
                post_meal_sugar: postMealSugar
            })
        })
        .then(response => response.json())
        .then(() => {
            // Fetch averages
            return fetch('/get_averages');
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Not enough data');
            }
            return response.json();
        })
        .then(averages => {
            // Update averages display
            fastingAverage.textContent = averages.fasting_average.toFixed(2);
            postMealAverage.textContent = averages.post_meal_average.toFixed(2);
            
            // Show averages section
            averagesSection.style.display = 'block';

            // Create/update chart
            createSugarChart(averages);

            // Clear inputs
            fastingSugarInput.value = '';
            postMealSugarInput.value = '';
        })
        .catch(error => {
            sugarErrorMessage.textContent = error.message;
        });
    });

    // Clear sugar data
    clearSugarBtn.addEventListener('click', async () => {
        try {
            await fetch('/clear_sugar_data', { method: 'POST' });
            
            // Hide averages section
            averagesSection.style.display = 'none';
            
            // Reset to empty chart rather than destroying
            createSugarChart(emptyAverages);
            
            sugarErrorMessage.textContent = '';
        } catch (error) {
            sugarErrorMessage.textContent = 'Failed to clear sugar data';
        }
    });

    // ========== BLOOD PRESSURE TRACKER ==========
    const systolicInput = document.getElementById('systolic');
    const diastolicInput = document.getElementById('diastolic');
    const submitBpBtn = document.getElementById('submit-bp-btn');
    const bpResultDiv = document.getElementById('bp-result');
    const readingsBody = document.getElementById('readings-body');
    const clearBpBtn = document.getElementById('clear-bp-btn');
    const bpChartCanvas = document.getElementById('bp-chart');
    let bpChart = null;

    // Create an empty BP chart initially
    function createEmptyBpChart() {
        const ctx = bpChartCanvas.getContext('2d');
        const labels = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'];
        
        if (bpChart) {
            bpChart.destroy();
        }
        
        bpChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Systolic',
                        data: Array(labels.length).fill(null),
                        borderColor: 'blue',
                        backgroundColor: 'rgba(0, 0, 255, 0.1)',
                        fill: false
                    },
                    {
                        label: 'Diastolic',
                        data: Array(labels.length).fill(null),
                        borderColor: 'red',
                        backgroundColor: 'rgba(255, 0, 0, 0.1)',
                        fill: false
                    },
                    {
                        label: 'Normal Systolic Max',
                        data: Array(labels.length).fill(120),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Normal Diastolic Max',
                        data: Array(labels.length).fill(80),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Blood Pressure Tracking'
                    },
                    legend: {
                        display: true
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'mmHg'
                        },
                        min: 40,  // Set minimum to show a good range
                        max: 180  // Set maximum to show normal ranges clearly
                    }
                }
            }
        });
    }

    // Initialize empty BP chart right away
    createEmptyBpChart();

    // Validation function for BP
    function validateBpInput(systolic, diastolic) {
        const systolicNum = parseInt(systolic, 10);
        const diastolicNum = parseInt(diastolic, 10);

        if (isNaN(systolicNum) || isNaN(diastolicNum)) {
            throw new Error('Please enter valid numeric values');
        }

        if (systolicNum <= 0 || diastolicNum <= 0 || 
            systolicNum > 300 || diastolicNum > 300) {
            throw new Error('Blood pressure values must be between 1 and 300 mmHg');
        }

        return { systolicNum, diastolicNum };
    }

    // Function to render BP readings in table
    function renderReadings(readings) {
        if (!Array.isArray(readings)) {
            console.error('Invalid readings data:', readings);
            return;
        }

        readingsBody.innerHTML = '';
        readings.forEach(reading => {
            if (!reading || typeof reading !== 'object') {
                console.warn('Invalid reading:', reading);
                return;
            }

            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${reading.timestamp || 'N/A'}</td>
                <td>${reading.systolic || 'N/A'}</td>
                <td>${reading.diastolic || 'N/A'}</td>
                <td class="${reading.status || ''}">${reading.category || 'Unknown'}</td>
            `;
            readingsBody.appendChild(row);
        });
    }

    // Function to draw BP chart using Chart.js
    function drawBpChart(readings) {
        if (!Array.isArray(readings)) {
            console.error('Invalid readings data:', readings);
            createEmptyBpChart(); // Fall back to empty chart
            return;
        }

        if (readings.length === 0) {
            createEmptyBpChart(); // Create empty chart for no readings
            return;
        }

        // Extract data
        const dates = readings.map(r => r.timestamp ? r.timestamp.split(' ')[0] : 'N/A');
        const systolicData = readings.map(r => r.systolic);
        const diastolicData = readings.map(r => r.diastolic);

        // Destroy existing chart if it exists
        if (bpChart) {
            bpChart.destroy();
        }

        const ctx = bpChartCanvas.getContext('2d');
        bpChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: 'Systolic',
                        data: systolicData,
                        borderColor: 'blue',
                        backgroundColor: 'rgba(0, 0, 255, 0.1)',
                        fill: false
                    },
                    {
                        label: 'Diastolic',
                        data: diastolicData,
                        borderColor: 'red',
                        backgroundColor: 'rgba(255, 0, 0, 0.1)',
                        fill: false
                    },
                    {
                        label: 'Normal Systolic Max',
                        data: Array(dates.length).fill(120),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Normal Diastolic Max',
                        data: Array(dates.length).fill(80),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Blood Pressure Tracking'
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'mmHg'
                        },
                        min: 40,  // Set minimum
                        max: 180  // Set maximum to show normal ranges clearly
                    }
                }
            }
        });
    }

    // Submit blood pressure reading
    submitBpBtn.addEventListener('click', async () => {
        try {
            // Validate input
            const { systolicNum, diastolicNum } = validateBpInput(
                systolicInput.value, 
                diastolicInput.value
            );

            const response = await fetch('/record_bp', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    systolic: systolicNum,
                    diastolic: diastolicNum
                })
            });

            const data = await response.json();

            if (data.error) {
                bpResultDiv.textContent = data.error;
                bpResultDiv.className = 'result red';
                return;
            }

            // Show result
            const reading = data.reading;
            bpResultDiv.textContent = `BP Category: ${reading.category} | Systolic: ${reading.systolic} mmHg | Diastolic: ${reading.diastolic} mmHg`;
            bpResultDiv.className = `result ${reading.status}`;

            // Render readings and chart
            renderReadings(data.readings);
            drawBpChart(data.readings);

            // Reset form
            systolicInput.value = '';
            diastolicInput.value = '';

        } catch (error) {
            bpResultDiv.textContent = error.message || 'An error occurred. Please try again.';
            bpResultDiv.className = 'result red';
        }
    });

    // Clear BP readings
    clearBpBtn.addEventListener('click', async () => {
        try {
            await fetch('/clear_readings', { method: 'POST' });
            readingsBody.innerHTML = '';
            createEmptyBpChart(); // Show empty chart instead of destroying
            bpResultDiv.textContent = '';
            bpResultDiv.className = 'result';
        } catch (error) {
            console.error('Error clearing readings:', error);
            bpResultDiv.textContent = 'Failed to clear readings';
            bpResultDiv.className = 'result red';
        }
    });

    // Initial load of BP readings
    async function loadInitialReadings() {
        try {
            const response = await fetch('/get_readings');
            const readings = await response.json();
            renderReadings(readings);
            drawBpChart(readings); // This will now handle empty arrays too
        } catch (error) {
            console.error('Error loading readings:', error);
            createEmptyBpChart(); // Fall back to empty chart
        }
    }

    // Initialize both trackers
    loadInitialReadings();
    fetch('/get_averages')
        .then(response => response.json())
        .then(averages => {
            if (averages.fasting_average > 0) {
                fastingAverage.textContent = averages.fasting_average.toFixed(2);
                postMealAverage.textContent = averages.post_meal_average.toFixed(2);
                averagesSection.style.display = 'block';
                createSugarChart(averages);
            } else {
                // We already created an empty chart earlier
                // But hide the averages section
                averagesSection.style.display = 'none';
            }
        })
        .catch(error => {
            console.error('Error loading sugar data:', error);
            // The empty chart is already created in the healthyRange fetch
        });
});
