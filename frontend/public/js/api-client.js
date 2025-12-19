/**
 * Enhanced API Client for Property Management System
 * Provides centralized API communication with error handling, caching, and retry logic
 */

class APIClient {
    constructor() {
        this.baseURL = 'http://127.0.0.1:8000/api';
        this.token = localStorage.getItem('authToken');
        this.cache = new Map();
        this.cacheTimeout = 5 * 60 * 1000; // 5 minutes
        this.retryAttempts = 3;
        this.retryDelay = 1000; // 1 second
    }

    /**
     * Set authentication token
     */
    setToken(token) {
        this.token = token;
        localStorage.setItem('authToken', token);
    }

    /**
     * Clear authentication token
     */
    clearToken() {
        this.token = null;
        localStorage.removeItem('authToken');
        this.cache.clear();
    }

    /**
     * Get default headers for requests
     */
    getHeaders(contentType = 'application/json') {
        const headers = {
            'Content-Type': contentType
        };

        if (this.token) {
            headers['Authorization'] = `Token ${this.token}`;
        }

        return headers;
    }

    /**
     * Generate cache key for requests
     */
    getCacheKey(url, params = {}) {
        const paramString = Object.keys(params).length > 0 
            ? '?' + new URLSearchParams(params).toString() 
            : '';
        return `${url}${paramString}`;
    }

    /**
     * Check if cached data is still valid
     */
    isCacheValid(cacheEntry) {
        return Date.now() - cacheEntry.timestamp < this.cacheTimeout;
    }

    /**
     * Sleep function for retry delays
     */
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    /**
     * Make HTTP request with retry logic
     */
    async makeRequest(url, options = {}, attempt = 1) {
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    ...this.getHeaders(),
                    ...options.headers
                }
            });

            // Handle authentication errors
            if (response.status === 401) {
                this.clearToken();
                throw new Error('Authentication required. Please log in again.');
            }

            // Handle other HTTP errors
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || errorData.message || `HTTP ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            // Retry logic for network errors
            if (attempt < this.retryAttempts && this.isRetryableError(error)) {
                console.warn(`Request failed (attempt ${attempt}), retrying...`, error.message);
                await this.sleep(this.retryDelay * attempt);
                return this.makeRequest(url, options, attempt + 1);
            }
            throw error;
        }
    }

    /**
     * Check if error is retryable
     */
    isRetryableError(error) {
        return error.name === 'TypeError' || // Network errors
               error.message.includes('fetch') ||
               error.message.includes('network');
    }

    /**
     * GET request with caching
     */
    async get(endpoint, params = {}, useCache = true) {
        const url = `${this.baseURL}${endpoint}`;
        const cacheKey = this.getCacheKey(endpoint, params);

        // Check cache first
        if (useCache && this.cache.has(cacheKey)) {
            const cacheEntry = this.cache.get(cacheKey);
            if (this.isCacheValid(cacheEntry)) {
                return cacheEntry.data;
            }
        }

        // Add query parameters
        const queryString = Object.keys(params).length > 0 
            ? '?' + new URLSearchParams(params).toString() 
            : '';
        
        const data = await this.makeRequest(`${url}${queryString}`, {
            method: 'GET'
        });

        // Cache the response
        if (useCache) {
            this.cache.set(cacheKey, {
                data,
                timestamp: Date.now()
            });
        }

        return data;
    }

    /**
     * POST request
     */
    async post(endpoint, data = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const response = await this.makeRequest(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });

        // Invalidate related cache entries
        this.invalidateCache(endpoint);
        
        return response;
    }

    /**
     * PUT request
     */
    async put(endpoint, data = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const response = await this.makeRequest(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });

        // Invalidate related cache entries
        this.invalidateCache(endpoint);
        
        return response;
    }

    /**
     * PATCH request
     */
    async patch(endpoint, data = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const response = await this.makeRequest(url, {
            method: 'PATCH',
            body: JSON.stringify(data)
        });

        // Invalidate related cache entries
        this.invalidateCache(endpoint);
        
        return response;
    }

    /**
     * DELETE request
     */
    async delete(endpoint) {
        const url = `${this.baseURL}${endpoint}`;
        
        const response = await this.makeRequest(url, {
            method: 'DELETE'
        });

        // Invalidate related cache entries
        this.invalidateCache(endpoint);
        
        return response;
    }

    /**
     * Invalidate cache entries related to an endpoint
     */
    invalidateCache(endpoint) {
        const baseEndpoint = endpoint.split('/')[1]; // Get base resource
        const keysToDelete = [];
        
        for (const key of this.cache.keys()) {
            if (key.includes(baseEndpoint)) {
                keysToDelete.push(key);
            }
        }
        
        keysToDelete.forEach(key => this.cache.delete(key));
    }

    /**
     * Clear all cache
     */
    clearCache() {
        this.cache.clear();
    }

    /**
     * Upload file
     */
    async uploadFile(endpoint, file, additionalData = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const formData = new FormData();
        
        formData.append('file', file);
        Object.keys(additionalData).forEach(key => {
            formData.append(key, additionalData[key]);
        });

        return await this.makeRequest(url, {
            method: 'POST',
            headers: {
                'Authorization': this.token ? `Token ${this.token}` : undefined
            },
            body: formData
        });
    }
}

// Create global API client instance
const apiClient = new APIClient();

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = APIClient;
}