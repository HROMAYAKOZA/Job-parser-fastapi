document.addEventListener('DOMContentLoaded', (event) => {
    fetchAll();
});

function fetchAll() {
    fetch('http://127.0.0.1:8000/jobs', {
        method: 'GET',
    })
        .then(response => response.json())
        .then(data => {
            // displayItems(data);
            displayJobs(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function fetchItems() {
    const salary = document.getElementById('salary').value;
    const city = document.getElementById('city').value;
    const experience = document.getElementById('experience').value;
    const remote = document.getElementById('remote').checked;
    const req_resume = document.getElementById('req_resume').checked;

    const filters = {
        salary: salary,
        city: city,
        experience: experience,
        remote: remote,
        req_resume: req_resume
    };

    fetch('http://127.0.0.1:8000/jobs_f', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filters),
    })
        .then(response => response.json())
        .then(data => {
            // displayItems(data);
            displayJobs(data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function displayJobs(jobs) {
    var loadingElement = document.querySelector('tr.loading');
    if (loadingElement) {
        loadingElement.remove();
    }
    const jobTableBody = document.querySelector('#jobTable tbody');
    jobTableBody.innerHTML = '';
    jobs.forEach(job => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td><a href="${job.link}" target="_blank">${job.title}</a></td>
            <td>${job.min_price} ₽</td>
            <td>${job.experience ? (job.experience > 3 ? job.experience + '+ лет' : job.experience + '+ год' + (job.experience > 1 ? 'а' : '')) : 'Без опыта'}</td>
            <td>${job.city}</td>
            <td>${job.remote ? '✅' : '❌'}</td>
            <td>${job.req_resume ? '✅' : '❌'}</td>
        `;

        jobTableBody.appendChild(row);
    });
}