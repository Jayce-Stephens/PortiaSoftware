function callBackend() {
    fetch('/model_test', {
      method: 'POST', // or 'GET' depending on your backend
    })
    .then(response => response.text())
    .then(data => {
      console.log('Backend says:', data);
      alert(data);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }