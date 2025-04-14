document.getElementById('scan-button').addEventListener('click', function () {
    let container = document.querySelector('.network-status');

    setTimeout(() => {
        container.innerHTML = 'Scanning...';
    }, 10000);
});