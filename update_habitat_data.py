#!/usr/bin/env python3
"""
Update script to populate habitat data for existing Pokemon
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.models.pokemon import db, Pokemon
from app.services.pokeapi_service import PokeAPIService

def update_pokemon_habitats():
    """Update habitat data for Pokemon that don't have it"""
    app = create_app()
    
    with app.app_context():
        pokeapi = PokeAPIService()
        
        # Find Pokemon without habitat data
        pokemon_without_habitat = Pokemon.query.filter(
            (Pokemon.habitat == None) | (Pokemon.habitat == '')
        ).all()
        
        print(f"Found {len(pokemon_without_habitat)} Pokemon without habitat data")
        
        updated_count = 0
        for pokemon in pokemon_without_habitat:
            try:
                print(f"Updating habitat for {pokemon.nickname} (Species ID: {pokemon.species_id})")
                
                # Get habitat from PokeAPI
                pokeapi_data = pokeapi.get_pokemon_data(pokemon.species_id)
                
                if pokeapi_data and pokeapi_data.get('habitat'):
                    pokemon.habitat = pokeapi_data['habitat']
                    updated_count += 1
                    print(f"  → Set habitat to: {pokemon.habitat}")
                else:
                    # Set a default habitat based on species type
                    types = pokemon.get_types()
                    default_habitat = 'unknown'
                    
                    if 'Water' in types:
                        default_habitat = 'waters-edge'
                    elif 'Rock' in types or 'Ground' in types:
                        default_habitat = 'cave'
                    elif 'Grass' in types:
                        default_habitat = 'forest'
                    elif 'Electric' in types:
                        default_habitat = 'urban'
                    
                    pokemon.habitat = default_habitat
                    updated_count += 1
                    print(f"  → Set default habitat to: {pokemon.habitat}")
                
            except Exception as e:
                print(f"  ❌ Error updating {pokemon.nickname}: {e}")
                pokemon.habitat = 'unknown'
        
        try:
            db.session.commit()
            print(f"\n✅ Successfully updated habitat data for {updated_count} Pokemon")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error saving changes: {e}")

if __name__ == "__main__":
    update_pokemon_habitats()