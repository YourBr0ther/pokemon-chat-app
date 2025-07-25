// Chat page JavaScript

let currentPokemon = null;
let currentTeam = [];

// Type gradient mappings
const typeGradients = {
    fire: 'linear-gradient(135deg, #FF6B35, #F7931E)',
    water: 'linear-gradient(135deg, #4FC3F7, #29B6F6)',
    grass: 'linear-gradient(135deg, #66BB6A, #4CAF50)',
    electric: 'linear-gradient(135deg, #FFEB3B, #FFC107)',
    psychic: 'linear-gradient(135deg, #E91E63, #9C27B0)',
    ice: 'linear-gradient(135deg, #81D4FA, #4FC3F7)',
    dragon: 'linear-gradient(135deg, #7C4DFF, #3F51B5)',
    dark: 'linear-gradient(135deg, #6D4C41, #3E2723)',
    fairy: 'linear-gradient(135deg, #F8BBD9, #E1BEE7)',
    fighting: 'linear-gradient(135deg, #D32F2F, #B71C1C)',
    poison: 'linear-gradient(135deg, #9C27B0, #7B1FA2)',
    ground: 'linear-gradient(135deg, #D7CCC8, #A1887F)',
    flying: 'linear-gradient(135deg, #B39DDB, #9575CD)',
    bug: 'linear-gradient(135deg, #8BC34A, #689F38)',
    rock: 'linear-gradient(135deg, #BCAAA4, #8D6E63)',
    ghost: 'linear-gradient(135deg, #7986CB, #5C6BC0)',
    steel: 'linear-gradient(135deg, #B0BEC5, #90A4AE)',
    normal: 'linear-gradient(135deg, #BDBDBD, #9E9E9E)'
};

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    loadTeam();
    
    // Check if specific Pokemon was requested via URL params
    const urlParams = new URLSearchParams(window.location.search);
    const pokemonId = urlParams.get('pokemon');
    if (pokemonId) {
        setTimeout(() => selectPokemon(parseInt(pokemonId)), 500);
    }
    
    // Initialize mobile gestures
    initializeMobileGestures();
    
    // Setup mobile/desktop responsive behavior
    setupResponsiveLayout();
});

// Mobile gesture support
function initializeMobileGestures() {
    let touchStartX = 0;
    let touchStartY = 0;
    let touchEndX = 0;
    let touchEndY = 0;
    
    // Swipe down to open drawer from chat header
    const chatHeader = document.getElementById('chat-header');
    if (chatHeader) {
        chatHeader.addEventListener('touchstart', (e) => {
            if (window.innerWidth > 968) return; // Only on mobile
            
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });
        
        chatHeader.addEventListener('touchend', (e) => {
            if (window.innerWidth > 968) return; // Only on mobile
            
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            handleHeaderSwipeGesture();
        }, { passive: true });
    }
    
    function handleHeaderSwipeGesture() {
        const swipeThreshold = 80;
        const verticalDistance = touchEndY - touchStartY;
        const horizontalDistance = Math.abs(touchStartX - touchEndX);
        
        // Swipe down gesture to open team drawer
        if (verticalDistance > swipeThreshold && horizontalDistance < verticalDistance) {
            const sidebar = document.getElementById('chat-sidebar');
            if (sidebar && !sidebar.classList.contains('show')) {
                openMobileTeam();
                
                // Add haptic feedback if available
                if (navigator.vibrate) {
                    navigator.vibrate(50);
                }
            }
        }
    }
    
    // Swipe up to close drawer
    const drawer = document.querySelector('.mobile-team-drawer');
    if (drawer) {
        drawer.addEventListener('touchstart', (e) => {
            touchStartX = e.changedTouches[0].screenX;
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });
        
        drawer.addEventListener('touchend', (e) => {
            touchEndX = e.changedTouches[0].screenX;
            touchEndY = e.changedTouches[0].screenY;
            handleDrawerSwipeGesture();
        }, { passive: true });
    }
    
    function handleDrawerSwipeGesture() {
        const swipeThreshold = 80;
        const verticalDistance = touchStartY - touchEndY;
        const horizontalDistance = Math.abs(touchStartX - touchEndX);
        
        // Swipe up gesture to close drawer
        if (verticalDistance > swipeThreshold && horizontalDistance < verticalDistance) {
            const sidebar = document.getElementById('chat-sidebar');
            if (sidebar && sidebar.classList.contains('show')) {
                closeMobileTeam();
                
                // Add haptic feedback if available
                if (navigator.vibrate) {
                    navigator.vibrate(30);
                }
            }
        }
    }
}

// Enhanced mobile touch feedback
function addTouchFeedback(element) {
    if (!element) return;
    
    element.addEventListener('touchstart', () => {
        element.style.transform = 'scale(0.95)';
        element.style.opacity = '0.8';
    }, { passive: true });
    
    element.addEventListener('touchend', () => {
        setTimeout(() => {
            element.style.transform = '';
            element.style.opacity = '';
        }, 150);
    }, { passive: true });
}

// Mobile team drawer functionality
function toggleMobileTeam() {
    const sidebar = document.getElementById('chat-sidebar');
    if (sidebar.classList.contains('show')) {
        closeMobileTeam();
    } else {
        openMobileTeam();
    }
}

function openMobileTeam() {
    const sidebar = document.getElementById('chat-sidebar');
    sidebar.classList.add('show');
    
    // Add event listener to close on background tap
    setTimeout(() => {
        document.addEventListener('click', handleMobileTeamBackdrop);
    }, 100);
}

function closeMobileTeam() {
    const sidebar = document.getElementById('chat-sidebar');
    sidebar.classList.remove('show');
    document.removeEventListener('click', handleMobileTeamBackdrop);
}

function handleMobileTeamBackdrop(e) {
    const drawer = document.querySelector('.mobile-team-drawer');
    const sidebar = document.getElementById('chat-sidebar');
    
    if (sidebar.classList.contains('show') && !drawer.contains(e.target)) {
        closeMobileTeam();
    }
}

// Responsive layout setup
function setupResponsiveLayout() {
    const mobileToggle = document.getElementById('mobile-team-toggle');
    
    function updateLayout() {
        const isMobile = window.innerWidth <= 968;
        
        if (isMobile) {
            // Show mobile toggle button when Pokemon is selected
            if (currentPokemon && mobileToggle) {
                mobileToggle.style.display = 'inline-block';
            }
        } else {
            // Hide mobile toggle on desktop
            if (mobileToggle) {
                mobileToggle.style.display = 'none';
            }
            closeMobileTeam();
        }
    }
    
    // Update on resize
    window.addEventListener('resize', updateLayout);
    updateLayout();
}

async function loadTeam() {
    try {
        const response = await apiRequest('/api/team/active');
        currentTeam = response.team;
        displayTeam();
    } catch (error) {
        console.error('Failed to load team:', error);
        showEmptyTeam();
    }
}

function displayTeam() {
    const teamList = document.getElementById('team-list');
    const sidebarEmpty = document.getElementById('sidebar-empty');
    
    if (currentTeam.length === 0) {
        showEmptyTeam();
        return;
    }
    
    sidebarEmpty.classList.add('hidden');
    
    teamList.innerHTML = currentTeam.map(teamMember => {
        const pokemon = teamMember.pokemon;
        const spriteUrl = pokemon.best_sprite || pokemon.sprite_url || 
                         `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.species_id}.png`;
        
        let specialBadge = '';
        if (pokemon.is_legendary) {
            specialBadge = '<span class="mini-badge legendary">⭐</span>';
        } else if (pokemon.is_mythical) {
            specialBadge = '<span class="mini-badge mythical">✨</span>';
        }
        
        return `
            <div class="team-member mobile-touch-target" onclick="selectPokemon(${pokemon.id})" data-pokemon-id="${pokemon.id}">
                <div class="member-sprite">
                    <img src="${spriteUrl}" alt="${pokemon.species_name}" class="member-sprite-img" 
                         onerror="this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.species_id}.png'">
                    ${specialBadge}
                </div>
                <div class="member-info">
                    <div class="member-name">${pokemon.nickname}</div>
                    <div class="member-species">${pokemon.species_name}</div>
                    ${pokemon.genus ? `<div class="member-genus">${pokemon.genus}</div>` : ''}
                    <div class="member-level">Level ${pokemon.level}</div>
                </div>
            </div>
        `;
    }).join('');
    
    // Add touch feedback to team members
    const teamMembers = document.querySelectorAll('.team-member');
    teamMembers.forEach(member => {
        addTouchFeedback(member);
    });
}

function showEmptyTeam() {
    document.getElementById('team-list').innerHTML = '';
    document.getElementById('sidebar-empty').classList.remove('hidden');
}

async function selectPokemon(pokemonId) {
    try {
        console.log('Selecting Pokemon with ID:', pokemonId);
        
        // Update UI to show selected Pokemon
        const teamMembers = document.querySelectorAll('.team-member');
        teamMembers.forEach(member => {
            member.classList.remove('active');
            if (parseInt(member.dataset.pokemonId) === pokemonId) {
                member.classList.add('active');
            }
        });
        
        // Load Pokemon data and chat history
        console.log('Making API request to:', `/api/pokemon/${pokemonId}/messages`);
        const response = await apiRequest(`/api/pokemon/${pokemonId}/messages`);
        console.log('API response received:', response);
        
        if (!response || !response.pokemon) {
            throw new Error('Invalid response format - missing pokemon data');
        }
        
        currentPokemon = response.pokemon;
        console.log('Current Pokemon set to:', currentPokemon.nickname);
        
        // Update chat header
        updateChatHeader();
        
        // Display chat history
        displayMessages(response.messages || []);
        
        // Show chat input
        const chatInputContainer = document.getElementById('chat-input-container');
        const clearChatBtn = document.getElementById('clear-chat-btn');
        const chatWelcome = document.getElementById('chat-welcome');
        
        if (chatInputContainer) chatInputContainer.style.display = 'flex';
        if (clearChatBtn) clearChatBtn.style.display = 'inline-block';
        if (chatWelcome) chatWelcome.classList.add('hidden');
        
        // Focus message input
        const messageInput = document.getElementById('message-input');
        if (messageInput) messageInput.focus();
        
        // Mobile-specific behavior
        const isMobile = window.innerWidth <= 968;
        if (isMobile) {
            // Close mobile team drawer
            closeMobileTeam();
            
            // Show mobile team toggle button
            const mobileToggle = document.getElementById('mobile-team-toggle');
            if (mobileToggle) {
                mobileToggle.style.display = 'inline-block';
            }
        }
        
        console.log('Pokemon selection completed successfully');
        
    } catch (error) {
        console.error('Error in selectPokemon:', error);
        showNotification(`Failed to load Pokemon chat: ${error.message}`, 'error');
    }
}

function updateChatHeader() {
    if (!currentPokemon) return;
    
    const nameElement = document.getElementById('current-pokemon-name');
    const detailsElement = document.getElementById('current-pokemon-details');
    const spriteElement = document.getElementById('current-pokemon-sprite');
    
    if (!nameElement || !detailsElement) {
        console.error('Chat header elements not found');
        return;
    }
    
    nameElement.textContent = `${currentPokemon.nickname} (${currentPokemon.species_name})`;
    
    let detailsText = `Level ${currentPokemon.level} • ${currentPokemon.nature} • ${formatFriendship(currentPokemon.friendship)} Friendship`;
    if (currentPokemon.genus) {
        detailsText = `${currentPokemon.genus} • ${detailsText}`;
    }
    
    // Apply type-based theming
    applyPokemonTheme();
    detailsElement.textContent = detailsText;
    
    // Update sprite if element exists
    if (spriteElement) {
        const spriteUrl = currentPokemon.best_sprite || currentPokemon.sprite_url || 
                         `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${currentPokemon.species_id}.png`;
        spriteElement.innerHTML = `
            <img src="${spriteUrl}" alt="${currentPokemon.species_name}" class="chat-header-sprite" 
                 onerror="this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${currentPokemon.species_id}.png'">
        `;
    }
}

function displayMessages(messages) {
    const chatMessages = document.getElementById('chat-messages');
    
    if (messages.length === 0) {
        chatMessages.innerHTML = `
            <div class="chat-welcome">
                <h3>Start a conversation with ${currentPokemon.nickname}!</h3>
                <p>Say hello or ask them how they're doing.</p>
            </div>
        `;
        return;
    }
    
    chatMessages.innerHTML = messages.map(message => {
        if (message.sender === 'user') {
            return `<div class="message user">${message.message}</div>`;
        } else {
            // Add nature and friendship data for Pokemon messages
            const nature = currentPokemon?.nature?.toLowerCase() || '';
            const friendshipLevel = getFriendshipLevel(currentPokemon?.friendship || 0);
            
            return `
                <div class="message pokemon friendship-${friendshipLevel}" 
                     data-nature="${nature}">
                    ${message.message}
                </div>
            `;
        }
    }).join('');
    
    // Scroll to bottom
    scrollToBottom();
}

function applyPokemonTheme() {
    if (!currentPokemon || !currentPokemon.types || currentPokemon.types.length === 0) return;
    
    const primaryType = currentPokemon.types[0].toLowerCase();
    const chatContainer = document.querySelector('.chat-container');
    const chatHeader = document.querySelector('.chat-header');
    const chatSprite = document.querySelector('.chat-pokemon-sprite');
    
    // Set type attribute for CSS styling
    if (chatContainer) {
        chatContainer.setAttribute('data-pokemon-type', primaryType);
    }
    
    // Apply type gradient as CSS variable
    const gradient = typeGradients[primaryType] || typeGradients.normal;
    document.documentElement.style.setProperty('--pokemon-type-gradient', gradient);
    
    // Add friendship-based glow intensity
    const friendshipLevel = getFriendshipLevel(currentPokemon.friendship);
    if (chatSprite) {
        chatSprite.classList.remove('friendship-low', 'friendship-medium', 'friendship-high');
        chatSprite.classList.add(`friendship-${friendshipLevel}`);
    }
}

function getFriendshipLevel(friendship) {
    if (friendship < 70) return 'low';
    if (friendship < 150) return 'medium';
    return 'high';
}

async function sendMessage(event) {
    event.preventDefault();
    
    if (!currentPokemon) {
        showNotification('Please select a Pokemon to chat with', 'error');
        return;
    }
    
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Clear input and disable form
    messageInput.value = '';
    messageInput.disabled = true;
    
    // Add user message to chat immediately
    addMessageToChat(message, 'user');
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Send message to API
        const response = await apiRequest(`/api/pokemon/${currentPokemon.id}/send`, {
            method: 'POST',
            body: JSON.stringify({ message })
        });
        
        // Hide typing indicator
        hideTypingIndicator();
        
        // Add Pokemon response to chat
        addMessageToChat(response.pokemon_response.message, 'pokemon');
        
        // Re-enable input
        messageInput.disabled = false;
        messageInput.focus();
        
    } catch (error) {
        hideTypingIndicator();
        messageInput.disabled = false;
        showNotification('Failed to send message', 'error');
        
        // Remove the user message if sending failed
        const messages = document.querySelectorAll('.message');
        const lastMessage = messages[messages.length - 1];
        if (lastMessage && lastMessage.classList.contains('user')) {
            lastMessage.remove();
        }
    }
}

function addMessageToChat(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    
    // Remove welcome message if present
    const welcome = chatMessages.querySelector('.chat-welcome');
    if (welcome) {
        welcome.remove();
    }
    
    // Create message element
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}`;
    messageElement.textContent = message;
    
    // Add to chat
    chatMessages.appendChild(messageElement);
    
    // Scroll to bottom
    scrollToBottom();
}

function showTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    const pokemonName = document.getElementById('typing-pokemon');
    
    if (currentPokemon) {
        // Customize typing message based on nature
        const nature = currentPokemon.nature?.toLowerCase() || '';
        let typingMessage = `${currentPokemon.nickname} is typing...`;
        
        // Nature-based typing variations
        if (['timid', 'quiet'].includes(nature)) {
            typingMessage = `${currentPokemon.nickname} is thinking...`;
        } else if (['bold', 'brave', 'adamant'].includes(nature)) {
            typingMessage = `${currentPokemon.nickname} is responding...`;
        } else if (['jolly', 'naive'].includes(nature)) {
            typingMessage = `${currentPokemon.nickname} is excited to reply...`;
        } else if (['calm', 'gentle'].includes(nature)) {
            typingMessage = `${currentPokemon.nickname} is composing a thoughtful response...`;
        }
        
        pokemonName.textContent = typingMessage;
    }
    
    indicator.classList.remove('hidden');
    scrollToBottom();
}

function hideTypingIndicator() {
    document.getElementById('typing-indicator').classList.add('hidden');
}

function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function clearChatHistory() {
    if (!currentPokemon) return;
    
    if (!confirm(`Clear all chat history with ${currentPokemon.nickname}?`)) {
        return;
    }
    
    try {
        const response = await apiRequest(`/api/pokemon/${currentPokemon.id}/clear-history`, {
            method: 'POST'
        });
        
        showNotification(response.message, 'success');
        
        // Clear messages display
        const chatMessages = document.getElementById('chat-messages');
        chatMessages.innerHTML = `
            <div class="chat-welcome">
                <h3>Start a fresh conversation with ${currentPokemon.nickname}!</h3>
                <p>Say hello or ask them how they're doing.</p>
            </div>
        `;
        
    } catch (error) {
        showNotification('Failed to clear chat history', 'error');
    }
}

// Handle Enter key in message input
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && e.target.id === 'message-input') {
        e.preventDefault();
        sendMessage(e);
    }
});