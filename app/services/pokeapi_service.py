import requests
import time
from typing import Dict, Optional, List
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)

class PokeAPIService:
    """Service for fetching Pokemon data from PokeAPI"""
    
    BASE_URL = "https://pokeapi.co/api/v2"
    CACHE_TIMEOUT = 3600  # 1 hour cache
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'PokemonChatApp/1.0'
        })
    
    @lru_cache(maxsize=1000)
    def get_pokemon_data(self, species_id: int) -> Optional[Dict]:
        """
        Get comprehensive Pokemon data from PokeAPI
        Returns sprite URLs, flavor text, stats, and more
        """
        try:
            # Fetch basic Pokemon data
            pokemon_response = self._make_request(f"/pokemon/{species_id}")
            if not pokemon_response:
                return None
            
            # Fetch species data for flavor text and more details
            species_response = self._make_request(f"/pokemon-species/{species_id}")
            
            return self._combine_pokemon_data(pokemon_response, species_response)
            
        except Exception as e:
            logger.error(f"Error fetching Pokemon data for ID {species_id}: {e}")
            return None
    
    def _make_request(self, endpoint: str, retries: int = 2) -> Optional[Dict]:
        """Make HTTP request with retry logic"""
        url = f"{self.BASE_URL}{endpoint}"
        
        for attempt in range(retries + 1):
            try:
                response = self.session.get(url, timeout=10)
                if response.status_code == 200:
                    return response.json()
                elif response.status_code == 404:
                    logger.warning(f"Pokemon not found: {endpoint}")
                    return None
                else:
                    logger.warning(f"API request failed: {response.status_code} for {endpoint}")
                    
            except requests.exceptions.RequestException as e:
                if attempt < retries:
                    time.sleep(1)  # Wait before retry
                    continue
                logger.error(f"Request failed after {retries + 1} attempts: {e}")
                
        return None
    
    def _combine_pokemon_data(self, pokemon_data: Dict, species_data: Optional[Dict]) -> Dict:
        """Combine Pokemon and species data into useful format"""
        combined = {
            'id': pokemon_data['id'],
            'name': pokemon_data['name'],
            'height': pokemon_data['height'],  # in decimeters
            'weight': pokemon_data['weight'],  # in hectograms
            'base_experience': pokemon_data.get('base_experience', 0),
            
            # Sprites
            'sprites': {
                'front_default': pokemon_data['sprites'].get('front_default'),
                'front_shiny': pokemon_data['sprites'].get('front_shiny'),
                'official_artwork': pokemon_data['sprites'].get('other', {}).get('official-artwork', {}).get('front_default'),
                'showdown': pokemon_data['sprites'].get('other', {}).get('showdown', {}).get('front_default'),
                'home': pokemon_data['sprites'].get('other', {}).get('home', {}).get('front_default')
            },
            
            # Base stats
            'base_stats': {
                stat['stat']['name']: stat['base_stat'] 
                for stat in pokemon_data.get('stats', [])
            },
            
            # Abilities
            'abilities': [
                {
                    'name': ability['ability']['name'],
                    'is_hidden': ability['is_hidden'],
                    'slot': ability['slot']
                }
                for ability in pokemon_data.get('abilities', [])
            ],
            
            # Types
            'types': [
                type_info['type']['name'] 
                for type_info in pokemon_data.get('types', [])
            ]
        }
        
        # Add species-specific data if available
        if species_data:
            combined.update(self._extract_species_data(species_data))
        
        return combined
    
    def _extract_species_data(self, species_data: Dict) -> Dict:
        """Extract interesting data from species endpoint"""
        species_info = {
            'genus': None,
            'flavor_text': None,
            'habitat': None,
            'color': species_data.get('color', {}).get('name'),
            'shape': species_data.get('shape', {}).get('name'),
            'generation': species_data.get('generation', {}).get('name'),
            'is_legendary': species_data.get('is_legendary', False),
            'is_mythical': species_data.get('is_mythical', False),
            'capture_rate': species_data.get('capture_rate', 45),
            'base_happiness': species_data.get('base_happiness', 50),
            'growth_rate': species_data.get('growth_rate', {}).get('name', 'medium')
        }
        
        # Get English flavor text (Pokédex entry)
        flavor_texts = species_data.get('flavor_text_entries', [])
        for entry in flavor_texts:
            if entry['language']['name'] == 'en':
                # Clean up the flavor text
                text = entry['flavor_text'].replace('\n', ' ').replace('\f', ' ')
                species_info['flavor_text'] = ' '.join(text.split())
                break
        
        # Get English genus (e.g., "Seed Pokémon")
        genera = species_data.get('genera', [])
        for genus in genera:
            if genus['language']['name'] == 'en':
                species_info['genus'] = genus['genus']
                break
        
        # Get habitat if available
        habitat = species_data.get('habitat')
        if habitat:
            species_info['habitat'] = habitat['name']
        
        return species_info
    
    def get_sprite_url(self, species_id: int, sprite_type: str = 'official_artwork') -> Optional[str]:
        """Get specific sprite URL for a Pokemon"""
        data = self.get_pokemon_data(species_id)
        if not data:
            return None
        
        sprites = data.get('sprites', {})
        return sprites.get(sprite_type) or sprites.get('front_default')
    
    def get_pokemon_description(self, species_id: int) -> Optional[str]:
        """Get Pokemon description/flavor text"""
        data = self.get_pokemon_data(species_id)
        if not data:
            return None
        
        return data.get('flavor_text')
    
    def clear_cache(self):
        """Clear the LRU cache"""
        self.get_pokemon_data.cache_clear()