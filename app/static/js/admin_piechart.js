document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('adminPieChart').getContext('2d');
    const totalDoctors = ctx.canvas.dataset.totalDoctors;
    const totalPatients = ctx.canvas.dataset.totalPatients;
    const totalAppointments = ctx.canvas.dataset.totalAppointments;

    const data = {
        labels: ['Doctors', 'Patients', 'Appointments'],
        datasets: [{
            data: [parseInt(totalDoctors), parseInt(totalPatients), parseInt(totalAppointments)],
            backgroundColor: ['#011c40','#254e97', '#00537A' ],
            borderColor: ['#011c40','#254e97', '#00537A' ],
            borderWidth: 1
        }]
    };

    const config = {
        type: 'pie',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                title: {
                    display: true,
                    text: 'Dashboard Overview'
                }
            }
        }
    };

    new Chart(ctx, config);
});
