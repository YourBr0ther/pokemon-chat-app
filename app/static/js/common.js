// Common JavaScript utilities

// Security functions
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function sanitizeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

function escapeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Configure default AJAX headers
function setupAjaxDefaults() {
    // Set up default headers for all AJAX requests
    const originalFetch = window.fetch;
    window.fetch = function(url, options = {}) {
        options.headers = options.headers || {};
        options.headers['X-CSRFToken'] = getCSRFToken();
        options.headers['Content-Type'] = options.headers['Content-Type'] || 'application/json';
        return originalFetch(url, options);
    };
}

// Show notification
function showNotification(message, type = 'success') {
    const notification = document.getElementById('notification');
    notification.textContent = sanitizeHTML(message); // Sanitize notification messages
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

// Format Pokemon types (safely)
function formatTypes(types) {
    return types.map(type => {
        const sanitizedType = escapeHTML(type);
        return `<span class="type-badge type-${sanitizedType.toLowerCase()}">${sanitizedType}</span>`;
    }).join(' ');
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
                console.log('PokeChat: Service Worker registered successfully');
                
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
    e.preventDefault();
    deferredPrompt = e;
    showInstallButton();
});

function showInstallButton() {
    // Don't show if already dismissed recently
    if (localStorage.getItem('pwa-install-dismissed')) {
        const dismissedTime = parseInt(localStorage.getItem('pwa-install-dismissed'));
        const daysSinceDismissed = (Date.now() - dismissedTime) / (1000 * 60 * 60 * 24);
        if (daysSinceDismissed < 7) { // Don't show again for 7 days
            return;
        }
    }
    
    // Create enhanced install banner if it doesn't exist
    if (!installButton) {
        const installBanner = document.createElement('div');
        installBanner.className = 'pwa-install-banner';
        installBanner.innerHTML = `
            <div class="install-banner-content">
                <div class="install-banner-icon">🚀</div>
                <div class="install-banner-text">
                    <div class="install-banner-title">Install PokeChat</div>
                    <div class="install-banner-subtitle">Get the full app experience with offline access</div>
                </div>
                <div class="install-banner-actions">
                    <button class="install-btn-primary" id="install-now">Install</button>
                    <button class="install-btn-secondary" id="install-later">Maybe Later</button>
                </div>
            </div>
        `;
        
        installBanner.style.cssText = `
            position: fixed;
            bottom: 20px;
            left: 20px;
            right: 20px;
            background: linear-gradient(135deg, var(--card), rgba(59, 130, 246, 0.1));
            backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: var(--radius-lg);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            z-index: 1000;
            animation: slideUp 0.5s ease-out;
            max-width: 400px;
            margin: 0 auto;
        `;
        
        // Add styles for banner components
        if (!document.getElementById('install-banner-styles')) {
            const style = document.createElement('style');
            style.id = 'install-banner-styles';
            style.textContent = `
                @keyframes slideUp {
                    from { transform: translateY(100px); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
                
                .install-banner-content {
                    display: flex;
                    align-items: center;
                    padding: var(--space-lg);
                    gap: var(--space-md);
                }
                
                .install-banner-icon {
                    font-size: 2rem;
                    flex-shrink: 0;
                }
                
                .install-banner-text {
                    flex: 1;
                    min-width: 0;
                }
                
                .install-banner-title {
                    font-weight: 600;
                    color: var(--text-primary);
                    font-size: 1rem;
                    margin-bottom: var(--space-xs);
                }
                
                .install-banner-subtitle {
                    font-size: 0.875rem;
                    color: var(--text-secondary);
                    line-height: 1.4;
                }
                
                .install-banner-actions {
                    display: flex;
                    flex-direction: column;
                    gap: var(--space-xs);
                    flex-shrink: 0;
                }
                
                .install-btn-primary {
                    background: linear-gradient(135deg, var(--primary-blue), var(--primary-purple));
                    color: white;
                    border: none;
                    padding: var(--space-sm) var(--space-md);
                    border-radius: var(--radius-md);
                    font-weight: 600;
                    font-size: 0.875rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    white-space: nowrap;
                }
                
                .install-btn-primary:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
                }
                
                .install-btn-secondary {
                    background: transparent;
                    color: var(--text-muted);
                    border: 1px solid rgba(203, 213, 225, 0.2);
                    padding: var(--space-xs) var(--space-sm);
                    border-radius: var(--radius-md);
                    font-size: 0.75rem;
                    cursor: pointer;
                    transition: all 0.3s ease;
                    white-space: nowrap;
                }
                
                .install-btn-secondary:hover {
                    background: rgba(203, 213, 225, 0.1);
                    color: var(--text-secondary);
                }
                
                @media (max-width: 480px) {
                    .pwa-install-banner {
                        left: 10px;
                        right: 10px;
                        bottom: 10px;
                    }
                    
                    .install-banner-content {
                        flex-direction: column;
                        text-align: center;
                        padding: var(--space-md);
                    }
                    
                    .install-banner-actions {
                        flex-direction: row;
                        justify-content: center;
                        width: 100%;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        // Event listeners
        installBanner.querySelector('#install-now').addEventListener('click', installPWA);
        installBanner.querySelector('#install-later').addEventListener('click', dismissInstallBanner);
        
        document.body.appendChild(installBanner);
        installButton = installBanner; // Store reference for later removal
        
        // Auto-hide after 30 seconds if not interacted with
        setTimeout(() => {
            if (installButton && installButton.parentNode) {
                dismissInstallBanner();
            }
        }, 30000);
    }
}

function dismissInstallBanner() {
    if (installButton && installButton.parentNode) {
        installButton.style.animation = 'slideDown 0.3s ease-in forwards';
        setTimeout(() => {
            installButton.remove();
            installButton = null;
        }, 300);
        
        // Remember dismissal
        localStorage.setItem('pwa-install-dismissed', Date.now().toString());
    }
    
    // Add slide down animation
    if (!document.getElementById('slide-down-animation')) {
        const style = document.createElement('style');
        style.id = 'slide-down-animation';
        style.textContent = `
            @keyframes slideDown {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(100px); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

async function installPWA() {
    if (!deferredPrompt) return;
    
    // Hide install banner
    if (installButton) {
        installButton.style.display = 'none';
    }
    
    try {
        // Show the install prompt
        deferredPrompt.prompt();
        
        const { outcome } = await deferredPrompt.userChoice;
        console.log(`PokeChat: User response to install prompt: ${outcome}`);
        
        if (outcome === 'accepted') {
            showInstallSuccessModal();
            
            // Track install analytics
            localStorage.setItem('pwa-installed', Date.now().toString());
            localStorage.removeItem('pwa-install-dismissed');
        } else {
            // User dismissed the install prompt
            dismissInstallBanner();
        }
        
        deferredPrompt = null;
    } catch (error) {
        console.error('PokeChat: Install failed:', error);
        showNotification('Installation failed. Please try again later.', 'error');
    }
}

// Show install success modal with onboarding
function showInstallSuccessModal() {
    const modal = document.createElement('div');
    modal.className = 'install-success-modal';
    modal.innerHTML = `
        <div class="install-success-content">
            <div class="install-success-header">
                <div class="install-success-icon">🎉</div>
                <h2>Welcome to PokeChat!</h2>
                <p>Your Pokemon app is now installed and ready to use</p>
            </div>
            <div class="install-success-features">
                <div class="feature-item">
                    <div class="feature-icon">📱</div>
                    <div class="feature-text">
                        <strong>Native App Experience</strong>
                        <span>Launch from your home screen just like any other app</span>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🔄</div>
                    <div class="feature-text">
                        <strong>Offline Access</strong>
                        <span>Chat with your Pokemon even without internet</span>
                    </div>
                </div>
                <div class="feature-item">
                    <div class="feature-icon">🔔</div>
                    <div class="feature-text">
                        <strong>Push Notifications</strong>
                        <span>Get notified when your Pokemon want to chat</span>
                    </div>
                </div>
            </div>
            <div class="install-success-actions">
                <button class="btn btn-primary" onclick="closeInstallSuccessModal()">Start Chatting!</button>
                <button class="btn btn-secondary" onclick="requestNotificationPermission()">Enable Notifications</button>
            </div>
        </div>
    `;
    
    modal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.8);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
        animation: fadeIn 0.3s ease-out;
        padding: var(--space-lg);
    `;
    
    // Add styles for success modal
    if (!document.getElementById('install-success-styles')) {
        const style = document.createElement('style');
        style.id = 'install-success-styles';
        style.textContent = `
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            .install-success-content {
                background: var(--card);
                border-radius: var(--radius-xl);
                padding: var(--space-2xl);
                max-width: 400px;
                width: 100%;
                box-shadow: 0 20px 40px rgba(0, 0, 0, 0.5);
                border: 1px solid rgba(59, 130, 246, 0.2);
                animation: slideUpFade 0.3s ease-out;
            }
            
            @keyframes slideUpFade {
                from { transform: translateY(50px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            
            .install-success-header {
                text-align: center;
                margin-bottom: var(--space-xl);
            }
            
            .install-success-icon {
                font-size: 3rem;
                margin-bottom: var(--space-md);
            }
            
            .install-success-header h2 {
                color: var(--text-primary);
                margin-bottom: var(--space-sm);
                font-size: 1.5rem;
            }
            
            .install-success-header p {
                color: var(--text-secondary);
                line-height: 1.5;
            }
            
            .install-success-features {
                margin-bottom: var(--space-xl);
            }
            
            .feature-item {
                display: flex;
                align-items: flex-start;
                gap: var(--space-md);
                margin-bottom: var(--space-lg);
            }
            
            .feature-icon {
                font-size: 1.5rem;
                flex-shrink: 0;
            }
            
            .feature-text {
                display: flex;
                flex-direction: column;
                gap: var(--space-xs);
            }
            
            .feature-text strong {
                color: var(--text-primary);
                font-weight: 600;
            }
            
            .feature-text span {
                color: var(--text-secondary);
                font-size: 0.875rem;
                line-height: 1.4;
            }
            
            .install-success-actions {
                display: flex;
                flex-direction: column;
                gap: var(--space-md);
            }
            
            .btn-secondary {
                background: transparent;
                border: 1px solid rgba(203, 213, 225, 0.2);
                color: var(--text-secondary);
            }
            
            .btn-secondary:hover {
                background: rgba(203, 213, 225, 0.1);
                color: var(--text-primary);
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(modal);
    
    // Auto close after 10 seconds
    setTimeout(() => {
        if (document.body.contains(modal)) {
            closeInstallSuccessModal();
        }
    }, 10000);
}

// Close install success modal
function closeInstallSuccessModal() {
    const modal = document.querySelector('.install-success-modal');
    if (modal) {
        modal.style.animation = 'fadeOut 0.3s ease-in forwards';
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
    
    // Add fade out animation
    if (!document.getElementById('fade-out-animation')) {
        const style = document.createElement('style');
        style.id = 'fade-out-animation';
        style.textContent = `
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

// Request notification permission
async function requestNotificationPermission() {
    if ('Notification' in window) {
        const permission = await Notification.requestPermission();
        if (permission === 'granted') {
            showNotification('Notifications enabled! Your Pokemon can now reach you anytime.', 'success');
            
            // Show a welcome notification
            new Notification('PokeChat Ready!', {
                body: 'Your Pokemon are excited to chat with you!',
                icon: '/static/icons/icon-192x192.png',
                tag: 'welcome-notification'
            });
        } else {
            showNotification('You can enable notifications later in your browser settings.', 'info');
        }
    }
    
    closeInstallSuccessModal();
}

// Handle successful installation
window.addEventListener('appinstalled', () => {
    console.log('PokeChat: PWA was installed');
    
    // Clean up install button
    if (installButton && installButton.parentNode) {
        installButton.remove();
        installButton = null;
    }
    
    // Mark as installed
    localStorage.setItem('pwa-installed', Date.now().toString());
    localStorage.removeItem('pwa-install-dismissed');
});

// App state management for PWA
function handlePWAState() {
    // Check if running as PWA (fullscreen or standalone)
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches || 
                        window.matchMedia('(display-mode: fullscreen)').matches ||
                        window.navigator.standalone === true;
    
    if (isStandalone) {
        document.body.classList.add('pwa-mode');
        console.log('PokeChat: Running in PWA standalone mode');
        
        // Handle viewport height for fullscreen mode
        const setViewportHeight = () => {
            const vh = window.innerHeight * 0.01;
            document.documentElement.style.setProperty('--vh', `${vh}px`);
        };
        
        setViewportHeight();
        window.addEventListener('resize', setViewportHeight);
        window.addEventListener('orientationchange', setViewportHeight);
    }
}

// Initialize common functionality
document.addEventListener('DOMContentLoaded', () => {
    setupAjaxDefaults(); // Setup CSRF protection for all AJAX requests
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