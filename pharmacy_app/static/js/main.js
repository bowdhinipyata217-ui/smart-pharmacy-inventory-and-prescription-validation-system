/**
 * Pharmacy AI - Main JavaScript
 * Handles client-side interactions and API calls
 */

// CSRF Token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// API Helper Functions
const API = {
    baseURL: '/api',
    
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            ...options,
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
                ...options.headers,
            },
        };
        
        // Add JWT token if available
        const token = localStorage.getItem('access_token');
        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },
    
    async uploadPrescription(file) {
        const formData = new FormData();
        formData.append('file', file);
        
        const token = localStorage.getItem('access_token');
        const headers = {
            'X-CSRFToken': csrftoken,
        };
        
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }
        
        const response = await fetch(`${this.baseURL}/prescriptions/upload/`, {
            method: 'POST',
            headers: headers,
            body: formData,
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Upload failed');
        }
        
        return await response.json();
    },
    
    async searchMedicine(query) {
        return this.request(`/medicines/search/?q=${encodeURIComponent(query)}`);
    },
    
    async getPrescriptionHistory() {
        return this.request('/prescriptions/history/');
    },
    
    async getMedicines() {
        return this.request('/medicines/');
    },
    
    async createMedicine(medicineData) {
        return this.request('/medicines/', {
            method: 'POST',
            body: JSON.stringify(medicineData),
        });
    },
    
    async updateMedicine(id, medicineData) {
        return this.request(`/medicines/${id}/`, {
            method: 'PUT',
            body: JSON.stringify(medicineData),
        });
    },
    
    async deleteMedicine(id) {
        return this.request(`/medicines/${id}/`, {
            method: 'DELETE',
        });
    },
};

// Utility Functions
const Utils = {
    showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        const container = document.querySelector('.main-content .container');
        if (container) {
            container.insertBefore(alertDiv, container.firstChild);
            
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
    },
    
    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit',
        });
    },
    
    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },
};

// Prescription Upload Handler
document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            const fileInput = document.getElementById('id_file');
            const file = fileInput.files[0];
            
            if (!file) {
                e.preventDefault();
                Utils.showAlert('Please select a file', 'error');
                return;
            }
            
            const submitBtn = document.getElementById('submitBtn');
            const spinner = document.getElementById('spinner');
            const progress = document.getElementById('progress');
            
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
            spinner.style.display = 'block';
            progress.style.display = 'block';

            // If user does NOT have a JWT token, do a normal form submit.
            // This uses Django session auth + template view (upload_prescription_view),
            // which is the expected flow for the HTML UI.
            const token = localStorage.getItem('access_token');
            if (!token) {
                return; // allow normal POST submit
            }

            // If JWT token exists, use the API endpoint instead.
            e.preventDefault();
            try {
                const result = await API.uploadPrescription(file);
                
                // Redirect to results page
                if (result.prescription_id) {
                    window.location.href = `/results/${result.prescription_id}/`;
                } else {
                    throw new Error('No prescription ID returned');
                }
            } catch (error) {
                Utils.showAlert(error.message || 'Error uploading prescription', 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Upload and Process';
                spinner.style.display = 'none';
                progress.style.display = 'none';
            }
        });
    }
    
    // Medicine search functionality
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        const debouncedSearch = Utils.debounce(async function(query) {
            if (query.length < 2) return;
            
            try {
                const results = await API.searchMedicine(query);
                // Handle search results (could display in dropdown, etc.)
                console.log('Search results:', results);
            } catch (error) {
                console.error('Search error:', error);
            }
        }, 300);
        
        searchInput.addEventListener('input', function(e) {
            debouncedSearch(e.target.value);
        });
    }
});

// Export for use in other scripts
window.PharmacyAI = {
    API,
    Utils,
};
