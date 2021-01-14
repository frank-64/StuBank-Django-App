var categories_config = {
    type: 'bar',
    data: {
        datasets: [{
            data: {
                {
                    category_data | safe
                }
            },
            backgroundColor: purple_fade,
            borderColor: purple,
            borderWidth: 1,
            label: 'Transactions'
        }],
        labels: {
            {
                category_labels | safe
            }
        }
    },
    options: {
        responsive: true,
        legend: {
            display: false
        },
        scales: {
            yAxes: [{
                scaleLabel: {
                    display: true,
                    labelString: 'Amount Spent - £'
                }
            }]
        }
    }
};