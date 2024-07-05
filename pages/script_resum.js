document.addEventListener('DOMContentLoaded', (event) => {
    fetchAll();
});

function fetchAll() {
    fetch('http://127.0.0.1:8000/resums', {
        method: 'GET',
    })
    .then(response => response.json())
    .then(data => {
        // displayItems(data);
        displayResums(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function fetchItems() {
    var max_salary = document.getElementById('max_salary').value;
    var experience = document.getElementById('experience').value;
    const status = document.getElementById('status').value;
    if (max_salary=='') {
        max_salary = 999999999
    }
    if (experience=='') {
        experience = 0
    }

    const filters = {
        max_salary: max_salary,
        experience: experience,
        status: status
    };

    fetch('http://127.0.0.1:8000/resums_f', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filters),
    })
    .then(response => response.json())
    .then(data => {
        // displayItems(data);
        displayResums(data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

function displayResums(resums) {
    var loadingElement = document.querySelector('tr.loading');
    if (loadingElement) {
        loadingElement.remove();
    }
    const resumTableBody = document.querySelector('#resumTable tbody');
    resumTableBody.innerHTML = '';
    resums.forEach(resum => {
        const row = document.createElement('tr');

        row.innerHTML = `
            <td><a href="${resum.link}" target="_blank">${resum.title}</a></td>
            <td>${resum.salary==null ? '<s>Неизвестно</s>' : resum.salary+' ₽'}</td>
            <td>${resum.experience ? (resum.experience>3 ? resum.experience+' лет' : resum.experience+' год'+(resum.experience>1 ? 'а' : '')) : 'Без опыта'}</td>
            <td>${resum.status==null ? '<s>Неизвестно</s>' : resum.status}</td>
            <td>${resum.last_company==null ? '<s>Неизвестно</s>' : resum.last_company}</td>
        `;

        resumTableBody.appendChild(row);
    });
}