document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('doctorPieChart').getContext('2d');
    const labels = ['Booked', 'Completed', 'Cancelled']; 
  
    const dataFromCanvas = ctx.canvas.dataset.data.split(',').map(x => parseInt(x, 10));

   
    const dataMap = {};
    dataFromCanvas.forEach((count, i) => {
        dataMap[labels[i]] = count;
    });

    const data = labels.map(label => dataMap[label] || 0);

    const backgroundColors = ['#254e97', '#00537a', '#011c40'];

    const chartData = {
        labels: labels,
        datasets: [{
            data: data,
            backgroundColor: backgroundColors,
            borderColor: '#fff',
            borderWidth: 2
        }]
    };

    const config = {
        type: 'pie',
        data: chartData,
        options: {
            responsive: true,
            plugins: {
                legend: { position: 'bottom' },
                datalabels: {
                    color: '#fff',
                    formatter: (value, ctx) => {
                        let sum = 0;
                        let dataArr = ctx.chart.data.datasets[0].data;
                        dataArr.forEach(data => sum += data);
                        let percentage = (value * 100 / sum).toFixed(1) + '%';
                        return percentage;
                    }
                }
            }
        },
        plugins: [ChartDataLabels]  
    };

    new Chart(ctx, config);
});
