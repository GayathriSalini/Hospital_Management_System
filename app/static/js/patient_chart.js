document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('patientLineChart').getContext('2d');
    const labels = ctx.canvas.dataset.labels.split(',');
    const data = ctx.canvas.dataset.values.split(',').map(x => parseInt(x, 10));

    const chartData = {
        labels: labels,
        datasets: [{
            label: 'No of Treatments Month',
            data: data,
            fill: false,
            borderColor: '#011c40',
            backgroundColor: '#011c40',
            tension: 0.3,
            pointRadius: 4,
            pointHoverRadius: 6
        }]
    };

    const config = {
        type: 'line',
        data: chartData,
        options: {
            responsive: true,
            scales: {
                x: {
                    title: { display: true, text: 'Month' }
                },
                y: {
                    title: { display: true, text: 'Number of Treatments' },
                    beginAtZero: true,
                    stepSize: 1
                }
            },
            plugins: {
                legend: { position: 'top' },
                title: { display: false }
            }
        }
    };

    new Chart(ctx, config);
});
