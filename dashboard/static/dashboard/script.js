document.addEventListener('DOMContentLoaded', function () {
    const canvas = document.getElementById('performanceChart');
    if (!canvas) return; // Safety check

    const ctx = canvas.getContext('2d');

    // Create a richer blue gradient for the area under the line
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 82, 204, 0.2)'); // Slightly deeper blue at top
    gradient.addColorStop(1, 'rgba(0, 82, 204, 0.00)'); // Fully transparent at bottom

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['EPOCH 01', 'EPOCH 04', 'EPOCH 08', 'CURRENT (V4.2.1)'],
            datasets: [{
                data: [0.35, 0.52, 0.45, 0.75], // Adjusted values for a more natural "wave" flow
                borderColor: '#0052cc',
                borderWidth: 3,
                pointBackgroundColor: '#ffffff',
                pointBorderColor: '#0052cc',
                pointBorderWidth: 2,
                pointRadius: 5, // Slightly larger points to match UI
                pointHoverRadius: 7,
                tension: 0.5, // INCREASED TENSION: Fixes the "strained" look for a smooth curve
                fill: true,
                backgroundColor: gradient,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#172b4d',
                    titleFont: { size: 12, family: 'Inter' },
                    bodyFont: { size: 12, family: 'Inter' },
                    cornerRadius: 8,
                    displayColors: false
                }
            },
            scales: {
                y: {
                    display: false,
                    beginAtZero: true,
                    max: 1 // Keeps the line within the top 75% of the box
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#8a94a6',
                        padding: 10,
                        font: {
                            size: 10,
                            weight: '700', // Matches the bold look of the UI labels
                            family: 'Inter'
                        }
                    }
                }
            },
            layout: {
                padding: {
                    top: 10,
                    bottom: 0,
                    left: 0,
                    right: 15 // Gives the final point a little room
                }
            }
        }
    });
});