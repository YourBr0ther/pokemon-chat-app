// Import page JavaScript

let currentPokemonData = null;
let currentPersonalityTraits = null;
let isImporting = false; // Global flag to prevent multiple imports

// Initialize drag and drop
document.addEventListener('DOMContentLoaded', () => {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    // Drag and drop events
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Click to select file
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });
});

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function handleFileSelect(e) {
    const files = e.target.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

async function processFile(file) {
    // Validate file type
    if (!file.name.toLowerCase().endsWith('.pk8')) {
        showNotification('Please select a .pk8 file', 'error');
        return;
    }
    
    // Validate file size (PK8 files are typically around 344 bytes but can vary)
    if (file.size < 300 || file.size > 400) {
        showNotification(`Invalid PK8 file size: ${file.size} bytes. Expected ~344 bytes.`, 'error');
        return;
    }
    
    // Show loading
    setLoading('loading-section', true);
    document.getElementById('preview-section').classList.add('hidden');
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        
        // Upload and parse file
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        // Store data for confirmation
        currentPokemonData = data.pokemon_data;
        currentPersonalityTraits = data.personality_traits;
        
        // Display preview
        displayPreview(data.pokemon_data, data.personality_traits);
        
        // Show preview section
        setLoading('loading-section', false);
        document.getElementById('preview-section').classList.remove('hidden');
        
    } catch (error) {
        setLoading('loading-section', false);
        showNotification(error.message, 'error');
    }
}

function displayPreview(pokemon, personality) {
    const previewDiv = document.getElementById('pokemon-preview');
    
    // Get the best sprite URL
    const spriteUrl = pokemon.official_artwork_url || pokemon.sprite_url || 
                     `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.species_id}.png`;
    
    // Create special badges for legendary/mythical
    let specialBadges = '';
    if (pokemon.is_legendary) {
        specialBadges += '<span class="badge legendary">⭐ Legendary</span>';
    }
    if (pokemon.is_mythical) {
        specialBadges += '<span class="badge mythical">✨ Mythical</span>';
    }
    
    previewDiv.innerHTML = `
        <div class="pokemon-info">
            <div class="pokemon-header">
                <div class="pokemon-sprite-section">
                    <img src="${spriteUrl}" alt="${pokemon.species_name}" class="pokemon-sprite" 
                         onerror="this.src='https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${pokemon.species_id}.png'">
                    ${specialBadges}
                </div>
                <div class="pokemon-title-section">
                    <h4>${pokemon.nickname} (${pokemon.species_name})</h4>
                    ${pokemon.genus ? `<p class="pokemon-genus">${pokemon.genus}</p>` : ''}
                    <div class="pokemon-types">
                        ${formatTypes(pokemon.types)}
                    </div>
                </div>
            </div>
            
            ${pokemon.description ? `
                <div class="pokemon-description">
                    <p><em>"${pokemon.description}"</em></p>
                </div>
            ` : ''}
            
            <div class="pokemon-details">
                <div class="detail-section">
                    <h5>Basic Info</h5>
                    <div class="details-grid">
                        <div><strong>Level:</strong> ${pokemon.level}</div>
                        <div><strong>Nature:</strong> ${pokemon.nature}</div>
                        <div><strong>Friendship:</strong> ${pokemon.friendship} (${formatFriendship(pokemon.friendship)})</div>
                        <div><strong>Trainer:</strong> ${pokemon.trainer_name}</div>
                        ${pokemon.height ? `<div><strong>Height:</strong> ${(pokemon.height / 10).toFixed(1)}m</div>` : ''}
                        ${pokemon.weight ? `<div><strong>Weight:</strong> ${(pokemon.weight / 10).toFixed(1)}kg</div>` : ''}
                        ${pokemon.habitat ? `<div><strong>Habitat:</strong> ${pokemon.habitat.charAt(0).toUpperCase() + pokemon.habitat.slice(1)}</div>` : ''}
                    </div>
                </div>
                
                <div class="detail-section">
                    <h5>Individual Values (IVs)</h5>
                    <div class="stats-grid">
                        ${formatStats(pokemon.ivs)}
                    </div>
                </div>
                
                ${pokemon.abilities && pokemon.abilities.length > 0 ? `
                    <div class="detail-section">
                        <h5>Abilities</h5>
                        <div class="abilities-list">
                            ${pokemon.abilities.map(ability => 
                                `<span class="ability-badge ${ability.is_hidden ? 'hidden-ability' : ''}">${ability.name.charAt(0).toUpperCase() + ability.name.slice(1).replace('-', ' ')}${ability.is_hidden ? ' (Hidden)' : ''}</span>`
                             ).join('')}
                        </div>
                    </div>
                ` : ''}
                
                ${pokemon.base_stats && Object.keys(pokemon.base_stats).length > 0 ? `
                    <div class="detail-section">
                        <h5>Base Stats</h5>
                        <div class="base-stats-grid">
                            ${formatBaseStats(pokemon.base_stats)}
                        </div>
                    </div>
                ` : ''}
                
                <div class="detail-section">
                    <h5>Personality Traits</h5>
                    <div class="personality-traits">
                        <div><strong>Species:</strong> ${personality.species_personality}</div>
                        <div><strong>Type Influence:</strong> ${personality.type_influence}</div>
                        <div><strong>Nature:</strong> ${personality.nature_traits}</div>
                        <div><strong>Friendship:</strong> ${personality.friendship_level}</div>
                        <div><strong>Maturity:</strong> ${personality.level_maturity}</div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

function formatBaseStats(baseStats) {
    const statNames = {
        'hp': 'HP',
        'attack': 'Attack',
        'defense': 'Defense',
        'special-attack': 'Sp. Attack',
        'special-defense': 'Sp. Defense',
        'speed': 'Speed'
    };
    
    return Object.entries(baseStats).map(([stat, value]) => {
        const displayName = statNames[stat] || stat.charAt(0).toUpperCase() + stat.slice(1);
        return `<div class="base-stat">
            <span class="stat-name">${displayName}:</span>
            <span class="stat-value">${value}</span>
            <div class="stat-bar">
                <div class="stat-fill" style="width: ${Math.min(100, (value / 255) * 100)}%"></div>
            </div>
        </div>`;
    }).join('');
}

function cancelImport() {
    // Clear data
    currentPokemonData = null;
    currentPersonalityTraits = null;
    isImporting = false; // Reset global flag
    
    // Reset UI
    document.getElementById('preview-section').classList.add('hidden');
    document.getElementById('file-input').value = '';
    
    // Reset button state
    const confirmBtn = document.getElementById('confirm-btn');
    if (confirmBtn) {
        confirmBtn.disabled = false;
        confirmBtn.dataset.saving = 'false';
        confirmBtn.textContent = 'Add to Pokedex';
    }
}

async function confirmImport(event) {
    if (!currentPokemonData || !currentPersonalityTraits) {
        showNotification('No Pokemon data to save', 'error');
        return;
    }
    
    // Prevent multiple imports with global flag
    if (isImporting) {
        console.log('Import already in progress');
        return;
    }
    
    // Prevent double-clicking and multiple submissions
    const confirmBtn = event ? event.target : document.getElementById('confirm-btn');
    if (confirmBtn.disabled || confirmBtn.dataset.saving === 'true') {
        console.log('Button already disabled or saving in progress');
        return;
    }
    
    // Mark as saving and disable button
    isImporting = true;
    confirmBtn.disabled = true;
    confirmBtn.dataset.saving = 'true';
    confirmBtn.textContent = 'Saving...';
    
    try {
        // Show loading
        setLoading('loading-section', true);
        document.getElementById('preview-section').classList.add('hidden');
        
        // Save Pokemon to database
        const response = await apiRequest('/api/save', {
            method: 'POST',
            body: JSON.stringify({
                pokemon_data: currentPokemonData,
                personality_traits: currentPersonalityTraits
            })
        });
        
        // Success - clear data immediately to prevent re-submission
        const savedPokemonName = currentPokemonData.nickname;
        currentPokemonData = null;
        currentPersonalityTraits = null;
        isImporting = false;
        
        showNotification(response.message, 'success');
        
        // Reset form
        cancelImport();
        setLoading('loading-section', false);
        
        // Optionally redirect to Pokedex
        setTimeout(() => {
            window.location.href = '/pokedex';
        }, 2000);
        
    } catch (error) {
        setLoading('loading-section', false);
        document.getElementById('preview-section').classList.remove('hidden');
        
        // Re-enable button on error only
        isImporting = false;
        confirmBtn.disabled = false;
        confirmBtn.dataset.saving = 'false';
        confirmBtn.textContent = 'Add to Pokedex';
        
        // Special handling for duplicate error
        if (error.message && error.message.includes('already in your Pokedex')) {
            showNotification(error.message, 'warning');
            // For duplicates, also clear the data to prevent confusion
            setTimeout(() => {
                cancelImport();
            }, 3000);
        } else {
            showNotification(error.message, 'error');
        }
    }
}