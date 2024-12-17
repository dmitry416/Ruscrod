import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://localhost:8000/api/',
});

apiClient.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('authToken');
        if (token) {
            config.headers['Authorization'] = `Token ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

apiClient.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response) {
            console.error('Server error:', error.response.data);
        } else if (error.request) {
            console.error('No response from server');
        } else {
            console.error('Request error:', error.message);
        }
        return Promise.reject(error);
    }
);

export default apiClient;