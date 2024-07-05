document.addEventListener('DOMContentLoaded', (event) => {
    fetchStatistics();
});

function fetchStatistics() {
    fetch('http://127.0.0.1:8000/statistics', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('jobs').innerText = `Вакансий: ${data.jobs}`;
        document.getElementById('resums').innerText = `Резюме: ${data.resums}`;
        document.getElementById('summ').innerText = `Всего: ${data.summ}`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
