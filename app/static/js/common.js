// Common JavaScript utilities

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type}`;
    notification.classList.remove('hidden');
    
    // Auto-hide after 3 seconds
    setTimeout(() => {
        notification.classList.add('hidden');
    }, 3000);
}

// Show/hide loading state
function setLoading(elementId, isLoading) {
    const element = document.getElementById(elementId);
    if (isLoading) {
        element.classList.remove('hidden');
    } else {
        element.classList.add('hidden');
    }
}

// Format Pokemon types
function formatTypes(types) {
    return types.map(type => 
        `<span class="type-badge type-${type.toLowerCase()}">${type}</span>`
    ).join(' ');
}

// Format Pokemon stats
function formatStats(ivs) {
    const statNames = {
        hp: 'HP',
        attack: 'Attack',
        defense: 'Defense',
        sp_attack: 'Sp. Att',
        sp_defense: 'Sp. Def',
        speed: 'Speed'
    };
    
    return Object.entries(ivs).map(([stat, value]) => 
        `<div class="stat">
            <div class="stat-name">${statNames[stat]}</div>
            <div class="stat-value">${value}</div>
        </div>`
    ).join('');
}

// Format friendship level
function formatFriendship(friendship) {
    if (friendship < 70) return 'Distant';
    if (friendship < 150) return 'Friendly';
    return 'Very Close';
}

// API request helper
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        return data;
    } catch (error) {
        console.error('API Request failed:', error);
        throw error;
    }
}

// Set active navigation link
function setActiveNavLink() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Initialize common functionality
document.addEventListener('DOMContentLoaded', () => {
    setActiveNavLink();
});

// Debounce function for search
function debounce(func, wait) {
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