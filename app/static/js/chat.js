// Chat page JavaScript

let currentPokemon = null;
let currentTeam = [];

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    loadTeam();
    
    // Check if specific Pokemon was requested via URL params
    const urlParams = new URLSearchParams(window.location.search);
    const pokemonId = urlParams.get('pokemon');
    if (pokemonId) {
        setTimeout(() => selectPokemon(parseInt(pokemonId)), 500);
    }
});

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
            <div class="team-member" onclick="selectPokemon(${pokemon.id})" data-pokemon-id="${pokemon.id}">
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
    
    chatMessages.innerHTML = messages.map(message => `
        <div class="message ${message.sender}">
            ${message.message}
        </div>
    `).join('');
    
    // Scroll to bottom
    scrollToBottom();
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
        pokemonName.textContent = `${currentPokemon.nickname} is typing...`;
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