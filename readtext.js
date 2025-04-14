fetch('anomalous_IPs.txt')
    .then(response => response.text())
    .then(data => {
        document.getElementById('banned-text').textContent = data;
    })
    .catch(error => {
        document.getElementById('banned-text').textContent = 'Error fetching the file.';
        console.error('Error fetching the file:', error);
    });
