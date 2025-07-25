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

// PWA functionality
let deferredPrompt;
let installButton;

// Service Worker Registration
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/sw.js')
            .then((registration) => {
                console.log('PokeChat: Service Worker registered successfully:', registration.scope);
                
                // Check for updates
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            showNotification('PokeChat has been updated! Refresh to get the latest version.', 'info');
                        }
                    });
                });
            })
            .catch((error) => {
                console.log('PokeChat: Service Worker registration failed:', error);
            });
    });
}

// PWA Install Prompt
window.addEventListener('beforeinstallprompt', (e) => {
    console.log('PokeChat: Install prompt triggered');
    e.preventDefault();
    deferredPrompt = e;
    showInstallButton();
});

function showInstallButton() {
    // Create install button if it doesn't exist
    if (!installButton) {
        installButton = document.createElement('button');
        installButton.innerHTML = '📱 Install App';
        installButton.className = 'install-btn';
        installButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--primary-blue), var(--primary-purple));
            color: white;
            border: none;
            padding: 12px 20px;
            border-radius: 25px;
            font-weight: 600;
            font-size: 0.875rem;
            cursor: pointer;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
            transition: all 0.3s ease;
            animation: installPulse 2s infinite;
        `;
        
        installButton.addEventListener('click', installPWA);
        document.body.appendChild(installButton);
        
        // Add CSS animation
        if (!document.getElementById('install-styles')) {
            const style = document.createElement('style');
            style.id = 'install-styles';
            style.textContent = `
                @keyframes installPulse {
                    0%, 100% { transform: scale(1); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
                    50% { transform: scale(1.05); box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5); }
                }
                .install-btn:hover {
                    transform: scale(1.05);
                    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5);
                }
            `;
            document.head.appendChild(style);
        }
    }
    
    installButton.style.display = 'block';
}

async function installPWA() {
    if (!deferredPrompt) return;
    
    installButton.style.display = 'none';
    deferredPrompt.prompt();
    
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`PokeChat: User response to install prompt: ${outcome}`);
    
    if (outcome === 'accepted') {
        showNotification('PokeChat installed successfully! 🎉', 'success');
    }
    
    deferredPrompt = null;
}

// Handle successful installation
window.addEventListener('appinstalled', () => {
    console.log('PokeChat: PWA was installed');
    showNotification('Welcome to PokeChat! The app is now installed on your device.', 'success');
    if (installButton) {
        installButton.style.display = 'none';
    }
});

// App state management for PWA
function handlePWAState() {
    // Check if running as PWA
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches || 
                        window.navigator.standalone === true;
    
    if (isStandalone) {
        document.body.classList.add('pwa-mode');
        console.log('PokeChat: Running in PWA mode');
    }
}

// Initialize common functionality
document.addEventListener('DOMContentLoaded', () => {
    setActiveNavLink();
    handlePWAState();
    
    // Add loading class to body initially
    document.body.classList.add('loading');
    
    // Remove loading class after content loads
    window.addEventListener('load', () => {
        setTimeout(() => {
            document.body.classList.remove('loading');
            document.body.classList.add('loaded');
        }, 300);
    });
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