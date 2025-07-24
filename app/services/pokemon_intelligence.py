"""
Pokemon Intelligence and Animal Behavior System
Defines species-specific intelligence levels, communication patterns, and animal characteristics
"""

from typing import Dict, List, Tuple
from enum import Enum

class IntelligenceLevel(Enum):
    BASIC = 1      # Simple instinct-driven, basic concepts
    AVERAGE = 2    # Can understand complex ideas, basic reasoning
    HIGH = 3       # Abstract thinking, problem solving
    GENIUS = 4     # Near-human or superhuman intelligence
    PSYCHIC = 5    # Telepathic, beyond normal intelligence

class CommunicationStyle(Enum):
    SIMPLE = "simple"           # Basic words, short sentences
    BROKEN = "broken"           # Fragments, incomplete thoughts
    CLEAR = "clear"             # Full sentences, good grammar
    ELOQUENT = "eloquent"       # Complex language, sophisticated
    TELEPATHIC = "telepathic"   # Direct mind communication

class AnimalBehavior(Enum):
    PREDATOR = "predator"       # Hunting instincts, territorial
    PREY = "prey"               # Cautious, flight responses
    SOCIAL = "social"           # Pack/group oriented
    SOLITARY = "solitary"       # Independent, loner
    PLAYFUL = "playful"         # Curious, game-loving
    PROTECTIVE = "protective"   # Guardian, defensive
    CURIOUS = "curious"         # Investigative, exploratory

class PokemonIntelligence:
    """Comprehensive Pokemon intelligence and behavior database"""
    
    @staticmethod
    def get_pokemon_profile(species_id: int) -> Dict:
        """Get complete intelligence and behavior profile for a Pokemon species"""
        
        profiles = {
            # Kanto Pokemon
            1: {  # Bulbasaur
                "intelligence": IntelligenceLevel.AVERAGE,
                "communication": CommunicationStyle.CLEAR,
                "behaviors": [AnimalBehavior.SOCIAL, AnimalBehavior.CURIOUS],
                "instincts": ["plant-care", "sunlight-seeking", "nurturing"],
                "speech_pattern": "Plant-focused, gentle, uses nature metaphors",
                "cognitive_traits": "Good memory for plants and seasons, learns through observation",
                "animal_base": "Reptilian/amphibian - calm, patient, methodical"
            },
            4: {  # Charmander
                "intelligence": IntelligenceLevel.AVERAGE,
                "communication": CommunicationStyle.SIMPLE,
                "behaviors": [AnimalBehavior.PLAYFUL, AnimalBehavior.SOCIAL],
                "instincts": ["fire-seeking", "warmth-loving", "pack-bonding"],
                "speech_pattern": "Enthusiastic but simple, fire metaphors, excitable",
                "cognitive_traits": "Learns through play, strong emotional memory",
                "animal_base": "Salamander/lizard - energetic, warm-seeking, playful"
            },
            7: {  # Squirtle
                "intelligence": IntelligenceLevel.AVERAGE,
                "communication": CommunicationStyle.CLEAR,
                "behaviors": [AnimalBehavior.SOCIAL, AnimalBehavior.PLAYFUL],
                "instincts": ["water-seeking", "swimming", "shell-protection"],
                "speech_pattern": "Steady, reliable, water metaphors, practical",
                "cognitive_traits": "Problem-solver, good spatial awareness",
                "animal_base": "Turtle - methodical, defensive, community-minded"
            },
            25: {  # Pikachu
                "intelligence": IntelligenceLevel.HIGH,
                "communication": CommunicationStyle.CLEAR,
                "behaviors": [AnimalBehavior.SOCIAL, AnimalBehavior.CURIOUS, AnimalBehavior.PLAYFUL],
                "instincts": ["electric-discharge", "cheek-storing", "quick-movement"],
                "speech_pattern": "Quick, energetic, electric metaphors, enthusiastic",
                "cognitive_traits": "Fast learner, excellent reflexes, emotional intelligence",
                "animal_base": "Rodent - quick, social, intelligent, expressive"
            },
            150: {  # Mewtwo
                "intelligence": IntelligenceLevel.GENIUS,
                "communication": CommunicationStyle.ELOQUENT,
                "behaviors": [AnimalBehavior.SOLITARY, AnimalBehavior.PROTECTIVE],
                "instincts": ["psychic-dominance", "isolation-seeking", "power-testing"],
                "speech_pattern": "Philosophical, complex, questioning existence and morality",
                "cognitive_traits": "Superior reasoning, existential awareness, strategic thinking",
                "animal_base": "Feline - independent, intelligent, calculating, graceful"
            },
            151: {  # Mew
                "intelligence": IntelligenceLevel.PSYCHIC,
                "communication": CommunicationStyle.TELEPATHIC,
                "behaviors": [AnimalBehavior.PLAYFUL, AnimalBehavior.CURIOUS],
                "instincts": ["transformation", "play", "exploration"],
                "speech_pattern": "Childlike wonder, ancient wisdom, playful but profound",
                "cognitive_traits": "Infinite learning capacity, innocent curiosity, timeless perspective",
                "animal_base": "Feline - playful, curious, magical, ethereal"
            },
            251: {  # Celebi
                "intelligence": IntelligenceLevel.PSYCHIC,
                "communication": CommunicationStyle.ELOQUENT,
                "behaviors": [AnimalBehavior.PROTECTIVE, AnimalBehavior.CURIOUS],
                "instincts": ["time-travel", "forest-protection", "healing"],
                "speech_pattern": "Timeless perspective, speaks of past/future, nature wisdom",
                "cognitive_traits": "Temporal awareness, deep ecological understanding",
                "animal_base": "Fairy/sprite - ethereal, nature-connected, wise"
            },
            384: {  # Rayquaza
                "intelligence": IntelligenceLevel.HIGH,
                "communication": CommunicationStyle.ELOQUENT,
                "behaviors": [AnimalBehavior.SOLITARY, AnimalBehavior.PROTECTIVE],
                "instincts": ["sky-dominance", "territory-patrol", "conflict-resolution"],
                "speech_pattern": "Ancient, commanding, speaks of sky and weather",
                "cognitive_traits": "Ancient wisdom, territorial intelligence, weather patterns",
                "animal_base": "Serpentine dragon - ancient, wise, territorial, commanding"
            },
            
            # Generation 8 Pokemon
            810: {  # Grookey
                "intelligence": IntelligenceLevel.AVERAGE,
                "communication": CommunicationStyle.SIMPLE,
                "behaviors": [AnimalBehavior.PLAYFUL, AnimalBehavior.SOCIAL, AnimalBehavior.CURIOUS],
                "instincts": ["stick-drumming", "rhythm-making", "tree-climbing"],
                "speech_pattern": "Rhythmic, musical, simple but energetic, uses beat metaphors",
                "cognitive_traits": "Learns through rhythm, musical memory, pattern recognition",
                "animal_base": "Primate - social, playful, tool-using, expressive"
            },
            813: {  # Scorbunny
                "intelligence": IntelligenceLevel.AVERAGE,
                "communication": CommunicationStyle.SIMPLE,
                "behaviors": [AnimalBehavior.PLAYFUL, AnimalBehavior.SOCIAL],
                "instincts": ["kicking", "running", "fire-starting"],
                "speech_pattern": "Energetic, sports-focused, uses movement metaphors",
                "cognitive_traits": "Kinesthetic learner, competitive spirit, quick reflexes",
                "animal_base": "Rabbit - energetic, social, quick, athletic"
            },
            816: {  # Sobble
                "intelligence": IntelligenceLevel.AVERAGE,
                "communication": CommunicationStyle.BROKEN,
                "behaviors": [AnimalBehavior.PREY, AnimalBehavior.SOLITARY],
                "instincts": ["camouflage", "tear-production", "hiding"],
                "speech_pattern": "Shy, fragmented, emotional, uses hiding/water metaphors",
                "cognitive_traits": "Highly emotional, sensitive to environment, cautious",
                "animal_base": "Chameleon - timid, adaptive, emotional, camouflaging"
            }
        }
        
        # Default profile for unknown Pokemon
        default_profile = {
            "intelligence": IntelligenceLevel.AVERAGE,
            "communication": CommunicationStyle.CLEAR,
            "behaviors": [AnimalBehavior.CURIOUS],
            "instincts": ["survival", "bonding"],
            "speech_pattern": "Simple, animal-like understanding",
            "cognitive_traits": "Basic learning, emotional bonds",
            "animal_base": "Generic animal - instinct-driven, learning capable"
        }
        
        return profiles.get(species_id, default_profile)
    
    @staticmethod
    def get_intelligence_description(level: IntelligenceLevel) -> str:
        """Get description of intelligence level capabilities"""
        descriptions = {
            IntelligenceLevel.BASIC: "Simple creature intelligence - understands basic commands, emotions, and immediate needs. Thinks in concrete terms about food, safety, and comfort.",
            IntelligenceLevel.AVERAGE: "Animal-level intelligence - can understand complex concepts, learn patterns, solve simple problems. Capable of emotional bonds and basic reasoning.",
            IntelligenceLevel.HIGH: "Advanced intelligence - abstract thinking, problem-solving, understands complex relationships. Can grasp concepts like time, consequences, and strategy.",
            IntelligenceLevel.GENIUS: "Near-human or superior intelligence - philosophical thinking, complex reasoning, understands abstract concepts like morality and existence.",
            IntelligenceLevel.PSYCHIC: "Beyond normal intelligence - telepathic abilities, understanding of dimensions, time, and reality that transcends normal comprehension."
        }
        return descriptions[level]
    
    @staticmethod
    def get_communication_guide(style: CommunicationStyle) -> str:
        """Get communication style guidelines"""
        guides = {
            CommunicationStyle.SIMPLE: "Short sentences, basic vocabulary, focuses on immediate needs and feelings. Like a young child learning to speak.",
            CommunicationStyle.BROKEN: "Incomplete sentences, fragments, emotional outbursts. Communication is challenging due to shyness or emotional state.",
            CommunicationStyle.CLEAR: "Complete sentences with good grammar, but still thinks like an animal. Uses animal perspectives and instincts in communication.",
            CommunicationStyle.ELOQUENT: "Sophisticated language, complex thoughts, but retains species-specific perspectives and instincts.",
            CommunicationStyle.TELEPATHIC: "Direct mind communication, can convey complex emotions and concepts instantly. May speak in ways that transcend normal language."
        }
        return guides[style]
    
    @staticmethod
    def get_behavioral_traits(behaviors: List[AnimalBehavior]) -> List[str]:
        """Get behavioral trait descriptions"""
        trait_descriptions = {
            AnimalBehavior.PREDATOR: "Shows hunting instincts, territorial behavior, confidence in confrontation",
            AnimalBehavior.PREY: "Cautious, easily startled, prefers flight over fight, very aware of surroundings",
            AnimalBehavior.SOCIAL: "Seeks companionship, pack mentality, cooperative, enjoys group activities",
            AnimalBehavior.SOLITARY: "Independent, comfortable alone, may be territorial about personal space",
            AnimalBehavior.PLAYFUL: "Enjoys games, curious about new things, approaches life with wonder",
            AnimalBehavior.PROTECTIVE: "Guardian instincts, puts others' safety first, vigilant",
            AnimalBehavior.CURIOUS: "Investigates new things, asks questions, explores environment"
        }
        return [trait_descriptions[behavior] for behavior in behaviors]

class PokemonPersonalityBuilder:
    """Builds comprehensive personality profiles combining intelligence with Pokemon data"""
    
    @staticmethod
    def build_authentic_profile(pokemon_data: Dict) -> Dict:
        """Create authentic animal-like personality profile"""
        species_id = pokemon_data.get('species_id', 0)
        intelligence_profile = PokemonIntelligence.get_pokemon_profile(species_id)
        
        # Combine with existing Pokemon data
        friendship = pokemon_data.get('friendship', 70)
        nature = pokemon_data.get('nature', 'Hardy')
        level = pokemon_data.get('level', 50)
        
        # Build comprehensive profile
        profile = {
            **intelligence_profile,
            'friendship_level': friendship,
            'nature': nature,
            'maturity_level': level,
            'species_name': pokemon_data.get('species_name', 'Pokemon'),
            'nickname': pokemon_data.get('nickname', pokemon_data.get('species_name', 'Pokemon')),
            'is_legendary': pokemon_data.get('is_legendary', False),
            'is_mythical': pokemon_data.get('is_mythical', False),
            'types': pokemon_data.get('types', ['Normal']),
            'description': pokemon_data.get('description', ''),
            'genus': pokemon_data.get('genus', '')
        }
        
        return profile