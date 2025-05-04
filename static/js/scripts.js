function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        // Simulate login process
        localStorage.setItem('username', username);
        window.location.href = 'upload.html';
    } else {
        alert('Please enter both username and password.');
    }
}

function handleFileUpload(event) {
    event.preventDefault();
    const fileType = document.querySelector('input[name="fileType"]:checked').value;
    const fileInput = document.getElementById('fileInput').files[0];

    if (fileType && fileInput) {
        // Simulate file upload process
        localStorage.setItem('uploadedFile', fileInput.name);
        localStorage.setItem('fileType', fileType);
        window.location.href = 'result.html';
    } else {
        alert('Please select a file and a type.');
    }
}

function displayResult() {
    const fileName = localStorage.getItem('uploadedFile');
    const fileType = localStorage.getItem('fileType');

    if (fileName && fileType) {
        document.getElementById('result').innerText = `Uploaded ${fileType}: ${fileName}`;
    } else {
        document.getElementById('result').innerText = 'No file uploaded.';
    }
}

document.getElementById('loginForm')?.addEventListener('submit', handleLogin);
document.getElementById('uploadForm')?.addEventListener('submit', handleFileUpload);
document.addEventListener('DOMContentLoaded', displayResult);

// Add button effects
document.querySelectorAll('button').forEach(button => {
    button.addEventListener('mouseover', () => {
        button.style.backgroundColor = '#00332e';
    });
    button.addEventListener('mouseout', () => {
        button.style.backgroundColor = '#004d40';
    });
});
