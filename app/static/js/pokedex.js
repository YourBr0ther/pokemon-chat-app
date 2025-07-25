// Pokedex page JavaScript

let allPokemon = [];
let currentTeam = [];

// Get type gradient for backgrounds
function getTypeGradient(type) {
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
    return typeGradients[type.toLowerCase()] || typeGradients.normal;
}

// Initialize page
document.addEventListener('DOMContentLoaded', () => {
    loadPokemon();
    loadTeam();
    setupSearch();
});

async function loadPokemon() {
    try {
        const response = await apiRequest('/api/pokemon');
        allPokemon = response.pokemon;
        
        if (allPokemon.length === 0) {
            showEmptyState();
        } else {
            displayPokemon(allPokemon);
        }
    } catch (error) {
        showNotification('Failed to load Pokemon', 'error');
    }
}

async function loadTeam() {
    try {
        const response = await apiRequest('/api/team');
        currentTeam = response.team;
        displayTeam();
        updateTeamCounter();
    } catch (error) {
        console.error('Failed to load team:', error);
    }
}

function displayPokemon(pokemon) {
    const grid = document.getElementById('pokemon-grid');
    const emptyState = document.getElementById('empty-state');
    
    if (pokemon.length === 0) {
        grid.innerHTML = '<p class="text-center">No Pokemon found</p>';
        return;
    }
    
    emptyState.classList.add('hidden');
    
    grid.innerHTML = pokemon.map(p => {
        const isInTeam = currentTeam.some(tm => tm.pokemon_id === p.id);
        const spriteUrl = p.best_sprite || p.sprite_url || 
                         `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.species_id}.png`;
        
        // Create special badges
        let specialBadges = '';
        if (p.is_legendary) {
            specialBadges += '<span class="badge legendary">⭐ Legendary</span>';
        }
        if (p.is_mythical) {
            specialBadges += '<span class="badge mythical">✨ Mythical</span>';
        }
        
        return `
            <div class="pokemon-card ${isInTeam ? 'in-team' : ''}" onclick="showPokemonDetails(${p.id})">
                <div class="pokemon-card-sprite">
                    <img src="${spriteUrl}" alt="${p.species_name}" class="pokemon-card-image" 
                         onerror="this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.species_id}.png'">
                    ${specialBadges}
                </div>
                <div class="pokemon-card-content">
                    <div class="pokemon-header">
                        <h4>${p.nickname}</h4>
                        <span class="species">${p.species_name}</span>
                        ${p.genus ? `<span class="genus">${p.genus}</span>` : ''}
                    </div>
                    <div class="pokemon-info">
                        <div class="level">Level ${p.level}</div>
                        <div class="types">${formatTypes(p.types)}</div>
                    </div>
                    <div class="pokemon-stats">
                        <div class="nature">${p.nature} Nature</div>
                        <div class="friendship">${formatFriendship(p.friendship)} Friendship</div>
                        ${p.height && p.weight ? `
                            <div class="physical-stats">
                                <span>${p.height_formatted}</span> • <span>${p.weight_formatted}</span>
                            </div>
                        ` : ''}
                    </div>
                    ${isInTeam ? '<div class="team-badge">On Team</div>' : ''}
                </div>
            </div>
        `;
    }).join('');
}

function displayTeam() {
    const teamGrid = document.getElementById('team-grid');
    
    // Create 6 slots
    const slots = [];
    for (let i = 1; i <= 6; i++) {
        const teamMember = currentTeam.find(tm => tm.slot_number === i);
        
        if (teamMember && teamMember.pokemon) {
            const p = teamMember.pokemon;
            const spriteUrl = p.best_sprite || p.sprite_url || 
                             `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.species_id}.png`;
            
            // Get primary type for background
            const primaryType = p.types[0] ? p.types[0].toLowerCase() : 'normal';
            const typeGradient = getTypeGradient(primaryType);
            
            slots.push(`
                <div class="team-slot filled type-${primaryType}" onclick="showPokemonDetails(${p.id})">
                    <div class="slot-number">#${i}</div>
                    <div class="pokemon-sprite-container">
                        <img src="${spriteUrl}" alt="${p.nickname}" class="pokemon-sprite"
                             onerror="this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.species_id}.png'">
                    </div>
                    <div class="pokemon-name">${p.nickname}</div>
                    <div class="pokemon-level">Lv.${p.level}</div>
                    <div class="pokemon-types">${formatTypes(p.types)}</div>
                </div>
            `);
        } else {
            slots.push(`
                <div class="team-slot">
                    <div class="slot-number">#${i}</div>
                    <div class="team-slot-empty">
                        <div class="team-slot-empty-icon">➕</div>
                        <div class="team-slot-empty-text">Empty</div>
                    </div>
                </div>
            `);
        }
    }
    
    teamGrid.innerHTML = slots.join('');
}

function updateTeamCounter() {
    const counter = document.getElementById('team-count');
    counter.textContent = `Team: ${currentTeam.length}/6`;
}

function showEmptyState() {
    document.getElementById('empty-state').classList.remove('hidden');
    document.getElementById('pokemon-grid').innerHTML = '';
}

async function showPokemonDetails(pokemonId) {
    try {
        const response = await apiRequest(`/api/pokemon/${pokemonId}`);
        const pokemon = response.pokemon;
        const isInTeam = currentTeam.some(tm => tm.pokemon_id === pokemon.id);
        
        const modalTitle = document.getElementById('modal-title');
        const modalBody = document.getElementById('modal-body');
        const modalActions = document.getElementById('modal-actions');
        
        modalTitle.textContent = `${pokemon.nickname} (${pokemon.species_name})`;
        
        modalBody.innerHTML = `
            <div class="pokemon-details-modal">
                <div class="detail-section">
                    <div class="types">${formatTypes(pokemon.types)}</div>
                </div>
                
                <div class="detail-section">
                    <h5>Basic Information</h5>
                    <div class="details-grid">
                        <div><strong>Level:</strong> ${pokemon.level}</div>
                        <div><strong>Nature:</strong> ${pokemon.nature}</div>
                        <div><strong>Friendship:</strong> ${pokemon.friendship} (${formatFriendship(pokemon.friendship)})</div>
                        <div><strong>Original Trainer:</strong> ${pokemon.original_trainer}</div>
                    </div>
                </div>
                
                <div class="detail-section">
                    <h5>Individual Values</h5>
                    <div class="stats-grid">
                        ${formatStats(pokemon.ivs)}
                    </div>
                </div>
                
                <div class="detail-section">
                    <h5>Personality Traits</h5>
                    <div class="personality-grid">
                        ${Object.entries(pokemon.personality || {}).map(([key, value]) => 
                            `<div><strong>${key.replace('_', ' ')}:</strong> ${value}</div>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
        
        // Action buttons
        const teamButton = isInTeam 
            ? `<button class="btn btn-secondary" onclick="removeFromTeam(${pokemon.id})">Remove from Team</button>`
            : `<button class="btn btn-primary" onclick="addToTeam(${pokemon.id})">Add to Team</button>`;
        
        modalActions.innerHTML = `
            ${teamButton}
            <button class="btn btn-secondary" onclick="goToChat(${pokemon.id})">Chat</button>
            <button class="btn btn-danger" onclick="deletePokemon(${pokemon.id})">Release</button>
        `;
        
        document.getElementById('pokemon-modal').classList.remove('hidden');
        
    } catch (error) {
        showNotification('Failed to load Pokemon details', 'error');
    }
}

async function addToTeam(pokemonId) {
    try {
        const response = await apiRequest('/api/team/add', {
            method: 'POST',
            body: JSON.stringify({ pokemon_id: pokemonId })
        });
        
        showNotification(response.message, 'success');
        closeModal();
        loadTeam();
        displayPokemon(allPokemon); // Refresh to show team status
        
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function removeFromTeam(pokemonId) {
    try {
        const response = await apiRequest('/api/team/remove', {
            method: 'POST',
            body: JSON.stringify({ pokemon_id: pokemonId })
        });
        
        showNotification(response.message, 'success');
        closeModal();
        loadTeam();
        displayPokemon(allPokemon); // Refresh to show team status
        
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

async function deletePokemon(pokemonId) {
    if (!confirm('Are you sure you want to release this Pokemon? This action cannot be undone.')) {
        return;
    }
    
    try {
        const response = await apiRequest(`/api/pokemon/${pokemonId}`, {
            method: 'DELETE'
        });
        
        showNotification(response.message, 'success');
        closeModal();
        loadPokemon();
        loadTeam();
        
    } catch (error) {
        showNotification(error.message, 'error');
    }
}

function goToChat(pokemonId) {
    window.location.href = `/chat?pokemon=${pokemonId}`;
}

function closeModal() {
    document.getElementById('pokemon-modal').classList.add('hidden');
}

function setupSearch() {
    const searchInput = document.getElementById('search-input');
    const debouncedSearch = debounce(performSearch, 300);
    
    searchInput.addEventListener('input', (e) => {
        debouncedSearch(e.target.value);
    });
}

function performSearch(query) {
    if (!query.trim()) {
        displayPokemon(allPokemon);
        return;
    }
    
    const filtered = allPokemon.filter(pokemon => 
        pokemon.nickname.toLowerCase().includes(query.toLowerCase()) ||
        pokemon.species_name.toLowerCase().includes(query.toLowerCase()) ||
        pokemon.nature.toLowerCase().includes(query.toLowerCase()) ||
        pokemon.types.some(type => type.toLowerCase().includes(query.toLowerCase()))
    );
    
    displayPokemon(filtered);
}

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modal = document.getElementById('pokemon-modal');
    if (e.target === modal) {
        closeModal();
    }
});