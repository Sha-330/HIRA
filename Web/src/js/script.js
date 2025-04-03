// Utility functions
function showMessage(message, type = 'info') {
    // Create notification element if it doesn't exist
    let notification = document.getElementById('notification');
    if (!notification) {
        notification = document.createElement('div');
        notification.id = 'notification';
        document.body.appendChild(notification);
    }
    
    // Set message and style based on type
    notification.textContent = message;
    notification.className = `notification ${type}`;
    
    // Show notification
    notification.style.display = 'block';
    
    // Hide after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
}

// Toggle mobile menu
function toggleMobileMenu() {
    const nav = document.querySelector('nav ul');
    nav.classList.toggle('show');
}

// Handle login process
function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        // Simulate login process
        localStorage.setItem('username', username);
        localStorage.setItem('isLoggedIn', 'true');
        showMessage('Login successful!', 'success');
        setTimeout(() => {
            window.location.href = 'upload.html';
        }, 1000);
    } else {
        showMessage('Please enter both username and password.', 'error');
    }
}

// File upload preview
function handleFileSelection() {
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    
    if (fileInput && fileInput.files.length > 0 && filePreview) {
        const file = fileInput.files[0];
        const fileName = document.createElement('p');
        fileName.innerHTML = `<i class="fas fa-file-medical"></i> ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
        
        // Clear previous preview
        filePreview.innerHTML = '';
        filePreview.appendChild(fileName);
        filePreview.style.display = 'block';
    }
}

// Handle file upload process
function handleFileUpload(event) {
    event.preventDefault();
    const fileTypeRadios = document.querySelectorAll('input[name="fileType"]');
    let fileType = null;
    
    // Find selected file type
    fileTypeRadios.forEach(radio => {
        if (radio.checked) {
            fileType = radio.value;
        }
    });
    
    const fileInput = document.getElementById('fileInput');
    
    if (fileType && fileInput && fileInput.files.length > 0) {
        const file = fileInput.files[0];
        
        // Simulate file upload process
        localStorage.setItem('uploadedFile', file.name);
        localStorage.setItem('fileType', fileType);
        localStorage.setItem('fileSize', file.size);
        localStorage.setItem('uploadDate', new Date().toISOString());
        
        showMessage('File uploaded successfully!', 'success');
        setTimeout(() => {
            window.location.href = 'result.html';
        }, 1000);
    } else {
        showMessage('Please select a file and a type.', 'error');
    }
}

// Display result with more details
function displayResult() {
    const resultElement = document.getElementById('result');
    
    if (!resultElement) return;
    
    const fileName = localStorage.getItem('uploadedFile');
    const fileType = localStorage.getItem('fileType');
    const fileSize = localStorage.getItem('fileSize');
    const uploadDate = localStorage.getItem('uploadDate');
    const username = localStorage.getItem('username');

    if (fileName && fileType) {
        // Create result card
        let resultHTML = `
            <div class="result-card">
                <h3><i class="fas fa-file-medical"></i> Analysis Results</h3>
                <div class="result-details">
                    <p><strong>File:</strong> ${fileName}</p>
                    <p><strong>Type:</strong> ${fileType}</p>
                    <p><strong>Size:</strong> ${(fileSize / 1024).toFixed(2)} KB</p>
                    <p><strong>Uploaded by:</strong> ${username || 'Unknown user'}</p>
                    <p><strong>Date:</strong> ${new Date(uploadDate).toLocaleString()}</p>
                </div>
                <div class="analysis-result">
                    <h4>Analysis Status</h4>
                    <div class="status-indicator">
                        <div class="status-bar">
                            <div class="status-progress"></div>
                        </div>
                        <p class="status-text">Analysis complete</p>
                    </div>
                    <p class="result-message">No abnormalities detected in the ${fileType.toLowerCase()} results.</p>
                </div>
                <div class="result-actions">
                    <button class="download-btn"><i class="fas fa-download"></i> Download Report</button>
                    <button class="share-btn"><i class="fas fa-share-alt"></i> Share Results</button>
                </div>
            </div>
        `;
        resultElement.innerHTML = resultHTML;
        
        // Animate progress bar
        setTimeout(() => {
            const progressBar = document.querySelector('.status-progress');
            if (progressBar) {
                progressBar.style.width = '100%';
            }
        }, 500);
        
        // Add event listeners for buttons
        document.querySelector('.download-btn')?.addEventListener('click', () => {
            showMessage('Report downloaded successfully!', 'success');
        });
        
        document.querySelector('.share-btn')?.addEventListener('click', () => {
            showMessage('Sharing options opened', 'info');
        });
        
    } else {
        resultElement.innerHTML = `
            <div class="empty-state">
                <i class="fas fa-file-upload"></i>
                <p>No file has been uploaded yet.</p>
                <a href="upload.html" class="btn primary-btn">Upload a File</a>
            </div>
        `;
    }
}

// Initialize event listeners and UI elements
document.addEventListener('DOMContentLoaded', function() {
    // Add mobile menu button event
    const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
    if (mobileMenuButton) {
        mobileMenuButton.addEventListener('click', toggleMobileMenu);
    }
    
    // Add notification container
    if (!document.getElementById('notification')) {
        const notification = document.createElement('div');
        notification.id = 'notification';
        notification.style.display = 'none';
        document.body.appendChild(notification);
    }
    
    // Check login status and update UI
    const isLoggedIn = localStorage.getItem('isLoggedIn') === 'true';
    const username = localStorage.getItem('username');
    
    // Update the nav links based on login status
    const loginLink = document.querySelector('a[href*="login.html"]');
    if (loginLink && isLoggedIn) {
        loginLink.innerHTML = `<i class="fas fa-sign-out-alt"></i> Logout (${username})`;
        loginLink.href = '#';
        loginLink.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('isLoggedIn');
            showMessage('Logged out successfully!', 'success');
            setTimeout(() => {
                window.location.href = loginLink.href.includes('../') ? '../../index.html' : 'index.html';
            }, 1000);
        });
    }
    
    // Setup form event listeners
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }
    
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFileUpload);
    }
    
    // Initialize file preview container
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', handleFileSelection);
        
        if (!document.getElementById('filePreview')) {
            const filePreview = document.createElement('div');
            filePreview.id = 'filePreview';
            filePreview.className = 'file-preview';
            filePreview.style.display = 'none';
            fileInput.parentNode.insertBefore(filePreview, fileInput.nextSibling);
        }
    }
    
    // Display results if on the results page
    displayResult();
    
    // Add hover effects to buttons
    document.querySelectorAll('button:not(.mobile-menu-toggle), .btn').forEach(button => {
        button.addEventListener('mouseover', () => {
            button.style.transform = 'translateY(-2px)';
        });
        button.addEventListener('mouseout', () => {
            button.style.transform = 'translateY(0)';
        });
    });
});
