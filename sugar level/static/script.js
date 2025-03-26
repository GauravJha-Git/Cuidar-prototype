document.addEventListener('DOMContentLoaded', () => {
    const fastingSugarInput = document.getElementById('fasting-sugar');
    const postMealSugarInput = document.getElementById('post-meal-sugar');
    const submitBtn = document.getElementById('submit-btn');
    const errorMessage = document.getElementById('error-message');
    const fastingAverage = document.getElementById('fasting-average');
    const postMealAverage = document.getElementById('post-meal-average');
    const averagesSection = document.getElementById('averages-section');
    let sugarChart = null;

    // Hide averages section initially
    averagesSection.style.display = 'none';

    // Fetch healthy range
    let healthyRange = {};
    fetch('/get_healthy_range')
        .then(response => response.json())
        .then(data => {
            healthyRange = data;
        });

    // Chart configuration
    function createSugarChart(averages) {
        const ctx = document.getElementById('sugar-chart').getContext('2d');
        
        // Destroy existing chart if it exists
        if (sugarChart) {
            sugarChart.destroy();
        }

        sugarChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
                datasets: [
                    {
                        label: 'Fasting Sugar Levels',
                        data: averages.fasting_levels,
                        borderColor: 'blue',
                        backgroundColor: 'rgba(0, 0, 255, 0.1)',
                        tension: 0.1
                    },
                    {
                        label: 'Post Meal Sugar Levels',
                        data: averages.post_meal_levels,
                        borderColor: 'red',
                        backgroundColor: 'rgba(255, 0, 0, 0.1)',
                        tension: 0.1
                    },
                    {
                        label: 'Healthy Fasting Min',
                        data: Array(5).fill(healthyRange.fasting_min),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Healthy Fasting Max',
                        data: Array(5).fill(healthyRange.fasting_max),
                        borderColor: 'green',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Healthy Post Meal Min',
                        data: Array(5).fill(healthyRange.post_meal_min),
                        borderColor: 'orange',
                        borderDash: [5, 5],
                        fill: false
                    },
                    {
                        label: 'Healthy Post Meal Max',
                        data: Array(5).fill(healthyRange.post_meal_max),
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
                    }
                },
                scales: {
                    y: {
                        title: {
                            display: true,
                            text: 'Sugar Level (mg/dL)'
                        }
                    }
                }
            }
        });
    }

    // Submit sugar levels
    submitBtn.addEventListener('click', () => {
        const fastingSugar = parseFloat(fastingSugarInput.value);
        const postMealSugar = parseFloat(postMealSugarInput.value);

        // Basic validation
        if (isNaN(fastingSugar) || isNaN(postMealSugar)) {
            errorMessage.textContent = 'Please enter valid sugar levels';
            return;
        }

        // Clear previous error
        errorMessage.textContent = '';

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
            errorMessage.textContent = error.message;
        });
    });
});