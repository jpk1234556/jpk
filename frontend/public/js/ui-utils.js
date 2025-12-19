/**
 * UI Utilities for Property Management System
 * Provides common UI functionality, notifications, and form handling
 */

class UIUtils {
    constructor() {
        this.loadingElements = new Set();
        this.notifications = [];
    }

    /**
     * Show loading spinner on element
     */
    showLoading(element, text = 'Loading...') {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (!element) return;

        this.loadingElements.add(element);
        element.disabled = true;
        
        const originalContent = element.innerHTML;
        element.setAttribute('data-original-content', originalContent);
        
        element.innerHTML = `
            <span class="loading-spinner"></span>
            ${text}
        `;
        
        element.classList.add('loading');
    }

    /**
     * Hide loading spinner from element
     */
    hideLoading(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        
        if (!element) return;

        this.loadingElements.delete(element);
        element.disabled = false;
        
        const originalContent = element.getAttribute('data-original-content');
        if (originalContent) {
            element.innerHTML = originalContent;
            element.removeAttribute('data-original-content');
        }
        
        element.classList.remove('loading');
    }

    /**
     * Show notification
     */
    showNotification(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-message">${message}</span>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">×</button>
            </div>
        `;

        // Add to notifications container or create one
        let container = document.querySelector('.notifications-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'notifications-container';
            document.body.appendChild(container);
        }

        container.appendChild(notification);
        this.notifications.push(notification);

        // Auto-remove after duration
        if (duration > 0) {
            setTimeout(() => {
                if (notification.parentElement) {
                    notification.remove();
                    this.notifications = this.notifications.filter(n => n !== notification);
                }
            }, duration);
        }

        return notification;
    }

    /**
     * Show success notification
     */
    showSuccess(message, duration = 5000) {
        return this.showNotification(message, 'success', duration);
    }

    /**
     * Show error notification
     */
    showError(message, duration = 8000) {
        return this.showNotification(message, 'error', duration);
    }

    /**
     * Show warning notification
     */
    showWarning(message, duration = 6000) {
        return this.showNotification(message, 'warning', duration);
    }

    /**
     * Show info notification
     */
    showInfo(message, duration = 5000) {
        return this.showNotification(message, 'info', duration);
    }

    /**
     * Clear all notifications
     */
    clearNotifications() {
        this.notifications.forEach(notification => {
            if (notification.parentElement) {
                notification.remove();
            }
        });
        this.notifications = [];
    }

    /**
     * Show confirmation dialog
     */
    async showConfirmation(message, title = 'Confirm Action') {
        return new Promise((resolve) => {
            const modal = document.createElement('div');
            modal.className = 'modal confirmation-modal';
            modal.innerHTML = `
                <div class="modal-content">
                    <div class="modal-header">
                        <h3>${title}</h3>
                    </div>
                    <div class="modal-body">
                        <p>${message}</p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary cancel-btn">Cancel</button>
                        <button class="btn btn-danger confirm-btn">Confirm</button>
                    </div>
                </div>
            `;

            document.body.appendChild(modal);
            modal.style.display = 'flex';

            const confirmBtn = modal.querySelector('.confirm-btn');
            const cancelBtn = modal.querySelector('.cancel-btn');

            confirmBtn.onclick = () => {
                modal.remove();
                resolve(true);
            };

            cancelBtn.onclick = () => {
                modal.remove();
                resolve(false);
            };

            // Close on backdrop click
            modal.onclick = (e) => {
                if (e.target === modal) {
                    modal.remove();
                    resolve(false);
                }
            };
        });
    }

    /**
     * Format date for display
     */
    formatDate(dateString, options = {}) {
        if (!dateString) return 'N/A';
        
        const date = new Date(dateString);
        const defaultOptions = {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        };
        
        return date.toLocaleDateString('en-US', { ...defaultOptions, ...options });
    }

    /**
     * Format currency
     */
    formatCurrency(amount, currency = 'USD') {
        if (amount === null || amount === undefined) return 'N/A';
        
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }

    /**
     * Format percentage
     */
    formatPercentage(value, decimals = 1) {
        if (value === null || value === undefined) return 'N/A';
        return `${Number(value).toFixed(decimals)}%`;
    }

    /**
     * Debounce function calls
     */
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
    }

    /**
     * Throttle function calls
     */
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    /**
     * Validate form fields
     */
    validateForm(form) {
        const errors = {};
        const formData = new FormData(form);
        
        // Get all required fields
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            const value = formData.get(field.name);
            if (!value || value.trim() === '') {
                errors[field.name] = 'This field is required';
            }
        });

        // Email validation
        const emailFields = form.querySelectorAll('input[type="email"]');
        emailFields.forEach(field => {
            const value = formData.get(field.name);
            if (value && !this.isValidEmail(value)) {
                errors[field.name] = 'Please enter a valid email address';
            }
        });

        // Password validation
        const passwordFields = form.querySelectorAll('input[type="password"]');
        passwordFields.forEach(field => {
            const value = formData.get(field.name);
            if (value && value.length < 8) {
                errors[field.name] = 'Password must be at least 8 characters long';
            }
        });

        return {
            isValid: Object.keys(errors).length === 0,
            errors
        };
    }

    /**
     * Display form errors
     */
    displayFormErrors(form, errors) {
        // Clear existing errors
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));

        // Display new errors
        Object.keys(errors).forEach(fieldName => {
            const field = form.querySelector(`[name="${fieldName}"]`);
            if (field) {
                field.classList.add('error');
                
                const errorElement = document.createElement('div');
                errorElement.className = 'error-message';
                errorElement.textContent = errors[fieldName];
                
                field.parentNode.insertBefore(errorElement, field.nextSibling);
            }
        });
    }

    /**
     * Clear form errors
     */
    clearFormErrors(form) {
        form.querySelectorAll('.error-message').forEach(el => el.remove());
        form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
    }

    /**
     * Validate email format
     */
    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Get form data as object
     */
    getFormData(form) {
        const formData = new FormData(form);
        const data = {};
        
        for (let [key, value] of formData.entries()) {
            data[key] = value;
        }
        
        return data;
    }

    /**
     * Populate form with data
     */
    populateForm(form, data) {
        Object.keys(data).forEach(key => {
            const field = form.querySelector(`[name="${key}"]`);
            if (field) {
                if (field.type === 'checkbox') {
                    field.checked = Boolean(data[key]);
                } else if (field.type === 'radio') {
                    const radioButton = form.querySelector(`[name="${key}"][value="${data[key]}"]`);
                    if (radioButton) {
                        radioButton.checked = true;
                    }
                } else {
                    field.value = data[key] || '';
                }
            }
        });
    }

    /**
     * Create pagination controls
     */
    createPagination(container, currentPage, totalPages, onPageChange) {
        if (typeof container === 'string') {
            container = document.querySelector(container);
        }

        if (!container || totalPages <= 1) return;

        const pagination = document.createElement('div');
        pagination.className = 'pagination';

        // Previous button
        if (currentPage > 1) {
            const prevBtn = document.createElement('button');
            prevBtn.textContent = 'Previous';
            prevBtn.className = 'btn btn-secondary';
            prevBtn.onclick = () => onPageChange(currentPage - 1);
            pagination.appendChild(prevBtn);
        }

        // Page numbers
        const startPage = Math.max(1, currentPage - 2);
        const endPage = Math.min(totalPages, currentPage + 2);

        for (let i = startPage; i <= endPage; i++) {
            const pageBtn = document.createElement('button');
            pageBtn.textContent = i;
            pageBtn.className = `btn ${i === currentPage ? 'btn-primary' : 'btn-secondary'}`;
            pageBtn.onclick = () => onPageChange(i);
            pagination.appendChild(pageBtn);
        }

        // Next button
        if (currentPage < totalPages) {
            const nextBtn = document.createElement('button');
            nextBtn.textContent = 'Next';
            nextBtn.className = 'btn btn-secondary';
            nextBtn.onclick = () => onPageChange(currentPage + 1);
            pagination.appendChild(nextBtn);
        }

        container.innerHTML = '';
        container.appendChild(pagination);
    }
}

// Create global UI utils instance
const uiUtils = new UIUtils();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UIUtils;
}