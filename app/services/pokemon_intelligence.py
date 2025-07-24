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

class LocationTraits(Enum):
    WILD_AREA = "wild_area"
    FOREST = "forest"
    CAVE = "cave"
    WATER = "water"
    MOUNTAIN = "mountain"
    CITY = "city"
    ROUTE = "route"
    UNKNOWN = "unknown"

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
        
        # Add location-based traits
        location_traits = PokemonPersonalityBuilder._get_location_traits(
            pokemon_data.get('habitat'), pokemon_data.get('species_id', 0)
        )
        
        # Get friendship-influenced nature reactions
        nature_reaction = PokemonPersonalityBuilder._get_friendship_nature_reaction(nature, friendship)
        
        # Build comprehensive profile
        profile = {
            **intelligence_profile,
            'friendship_level': friendship,
            'nature': nature,
            'nature_reaction': nature_reaction,
            'maturity_level': level,
            'species_name': pokemon_data.get('species_name', 'Pokemon'),
            'nickname': pokemon_data.get('nickname', pokemon_data.get('species_name', 'Pokemon')),
            'is_legendary': pokemon_data.get('is_legendary', False),
            'is_mythical': pokemon_data.get('is_mythical', False),
            'types': pokemon_data.get('types', ['Normal']),
            'description': pokemon_data.get('description', ''),
            'genus': pokemon_data.get('genus', ''),
            'location_traits': location_traits,
            'habitat': pokemon_data.get('habitat', 'unknown')
        }
        
        return profile
    
    @staticmethod
    def _get_location_traits(habitat: str, species_id: int) -> Dict:
        """Get personality traits based on where Pokemon was caught/lives"""
        
        # Map habitat to location traits
        habitat_traits = {
            'forest': {
                'environment': 'Dense woodlands with tall trees and undergrowth',
                'comfort_zone': 'Among trees, natural sounds, earth scents',
                'survival_skills': 'Climbing, foraging, hiding in vegetation',
                'social_patterns': 'Territorial or pack-based depending on species',
                'fears': 'Open spaces, loud noises, fire',
                'memories': 'Rustling leaves, bird calls, morning dew, seasonal changes'
            },
            'cave': {
                'environment': 'Dark underground tunnels and caverns',  
                'comfort_zone': 'Darkness, enclosed spaces, cool temperatures',
                'survival_skills': 'Echo-location, feeling through touch, mineral detection',
                'social_patterns': 'Often solitary or small family groups',
                'fears': 'Bright lights, loud echoing sounds, cave-ins',
                'memories': 'Dripping water, cool stone, echoing footsteps, mineral scents'
            },
            'waters-edge': {
                'environment': 'Rivers, lakes, ponds, and shorelines',
                'comfort_zone': 'Near water, humid air, muddy ground',
                'survival_skills': 'Swimming, fishing, water navigation',
                'social_patterns': 'Often social, gathering at water sources',
                'fears': 'Drought, pollution, being far from water',
                'memories': 'Flowing water, fish jumping, wet rocks, rain on water'
            },
            'mountain': {
                'environment': 'High altitude rocky peaks and cliffs',
                'comfort_zone': 'Thin air, rocky surfaces, wide views',
                'survival_skills': 'Climbing, wind resistance, altitude adaptation',
                'social_patterns': 'Independent, territorial about peaks',
                'fears': 'Landslides, storms, loss of footing',
                'memories': 'Wind howling, snow crunching, vast views, cold mornings'
            },
            'grassland': {
                'environment': 'Open fields and meadows',
                'comfort_zone': 'Open spaces, grass, gentle breezes',
                'survival_skills': 'Running, grazing, herd coordination',
                'social_patterns': 'Often herd animals, safety in numbers',
                'fears': 'Predators from above, storms with no shelter',
                'memories': 'Grass waving, flower scents, butterflies, warm sun'
            },
            'urban': {
                'environment': 'Cities and human settlements',
                'comfort_zone': 'Buildings, human presence, artificial lights',
                'survival_skills': 'Scavenging, avoiding traffic, human interaction',
                'social_patterns': 'Adapted to humans, often friendly',
                'fears': 'Wild predators, being abandoned, loud machinery',
                'memories': 'Car sounds, building lights, human voices, food scraps'
            }
        }
        
        # Get traits for habitat, default to unknown location
        location_data = habitat_traits.get(habitat, {
            'environment': 'Unknown environment',
            'comfort_zone': 'Familiar surroundings',
            'survival_skills': 'Basic survival instincts',
            'social_patterns': 'Species-typical behavior',
            'fears': 'Unfamiliar situations',
            'memories': 'Fragmented memories of home'
        })
        
        # Add species-specific location modifications
        if species_id in [25]:  # Pikachu
            if habitat == 'forest':
                location_data['memories'] = 'Electric storms, power lines in trees, berry bushes'
        elif species_id in [810, 811, 812]:  # Grookey line
            if habitat == 'forest':
                location_data['memories'] = 'Drumming on hollow logs, rhythm of rain on leaves'
        
        return {
            'habitat_type': habitat or 'unknown',
            **location_data
        }
    
    @staticmethod
    def _get_friendship_nature_reaction(nature: str, friendship: int) -> Dict:
        """Get how nature manifests differently based on friendship level"""
        
        # Define positive and negative aspects of each nature
        nature_reactions = {
            'Hardy': {
                'positive': 'Steadfast and reliable, shows quiet strength',
                'negative': 'Stubborn and inflexible, resists new experiences'
            },
            'Lonely': {
                'positive': 'Independent and self-reliant, values solitude for reflection',
                'negative': 'Withdrawn and melancholic, avoids social interaction'
            },
            'Brave': {
                'positive': 'Courageous protector, faces danger for others',
                'negative': 'Reckless and aggressive, starts unnecessary conflicts'
            },
            'Adamant': {
                'positive': 'Determined achiever, never gives up on goals',
                'negative': 'Stubborn and bullheaded, refuses to listen to others'
            },
            'Naughty': {
                'positive': 'Playfully mischievous, brings joy and laughter',
                'negative': 'Destructively troublesome, causes problems for attention'
            },
            'Bold': {
                'positive': 'Confident leader, inspires others with presence',
                'negative': 'Arrogant and pushy, dominates conversations'
            },
            'Docile': {
                'positive': 'Gentle and agreeable, easy to get along with',
                'negative': 'Overly submissive, lacks backbone in conflicts'
            },
            'Relaxed': {
                'positive': 'Calm and easygoing, helps others stay peaceful',
                'negative': 'Lazy and unmotivated, avoids responsibility'
            },
            'Impish': {
                'positive': 'Cleverly playful, entertains with harmless pranks',
                'negative': 'Maliciously mischievous, enjoys others\' discomfort'
            },
            'Lax': {
                'positive': 'Carefree and optimistic, doesn\'t worry about small things',
                'negative': 'Careless and irresponsible, ignores important matters'
            },
            'Timid': {
                'positive': 'Thoughtfully cautious, considers risks carefully',
                'negative': 'Fearful and anxious, paralyzed by uncertainty'
            },
            'Hasty': {
                'positive': 'Energetically quick, gets things done efficiently',
                'negative': 'Impatiently rushing, makes careless mistakes'
            },
            'Serious': {
                'positive': 'Focused and dedicated, takes responsibilities seriously',
                'negative': 'Grimly intense, unable to relax or have fun'
            },
            'Jolly': {
                'positive': 'Joyfully upbeat, spreads happiness to others',
                'negative': 'Annoyingly hyperactive, insensitive to others\' moods'
            },
            'Naive': {
                'positive': 'Innocently trusting, sees the best in everyone',
                'negative': 'Dangerously gullible, easily manipulated'
            },
            'Modest': {
                'positive': 'Humbly confident, doesn\'t boast about abilities',
                'negative': 'Self-deprecating, lacks confidence in own worth'
            },
            'Mild': {
                'positive': 'Gently kind, speaks softly and considerately',
                'negative': 'Passively weak, won\'t stand up for beliefs'
            },
            'Quiet': {
                'positive': 'Thoughtfully observant, listens before speaking',
                'negative': 'Antisocially silent, avoids communication'
            },
            'Bashful': {
                'positive': 'Sweetly shy, charmingly modest in interactions',
                'negative': 'Painfully awkward, hides from social situations'
            },
            'Rash': {
                'positive': 'Passionately expressive, shows emotions honestly',
                'negative': 'Explosively volatile, lashes out when upset'
            },
            'Calm': {
                'positive': 'Peacefully serene, maintains composure under pressure',
                'negative': 'Emotionally detached, seems uncaring about others'
            },
            'Gentle': {
                'positive': 'Lovingly nurturing, cares deeply for others\' wellbeing',
                'negative': 'Overly protective, smothers with excessive worry'
            },
            'Sassy': {
                'positive': 'Confidently spirited, stands up for beliefs with attitude',
                'negative': 'Rudely defiant, disrespects authority figures'
            },
            'Careful': {
                'positive': 'Wisely cautious, thinks through consequences',
                'negative': 'Anxiously paranoid, expects the worst outcomes'
            },
            'Quirky': {
                'positive': 'Uniquely creative, brings fresh perspectives',
                'negative': 'Weirdly unpredictable, makes others uncomfortable'
            }
        }
        
        nature_data = nature_reactions.get(nature, {
            'positive': 'Shows balanced temperament',
            'negative': 'Shows typical animal caution'
        })
        
        # Determine which aspect dominates based on friendship
        if friendship < 70:  # Wary/Untrusting - negative aspects dominate
            dominant_trait = nature_data['negative']
            subdued_trait = nature_data['positive']
            manifestation = 'defensive'
        elif friendship < 150:  # Warming up - mixed but moving toward positive
            dominant_trait = f"Slowly showing {nature_data['positive'].lower()}"
            subdued_trait = f"Still sometimes {nature_data['negative'].lower()}"
            manifestation = 'evolving'
        else:  # Loyal - positive aspects dominate
            dominant_trait = nature_data['positive']
            subdued_trait = f"Rarely {nature_data['negative'].lower()}"
            manifestation = 'trusting'
        
        return {
            'dominant_trait': dominant_trait,
            'subdued_trait': subdued_trait,
            'manifestation': manifestation,
            'nature_description': f"A {nature.lower()} Pokemon showing {manifestation} behavior"
        }
    
    @staticmethod
    def get_first_encounter_scenario(pokemon_data: Dict) -> Dict:
        """Generate first encounter scenario for newly imported Pokemon"""
        species_id = pokemon_data.get('species_id', 0)
        intelligence_profile = PokemonIntelligence.get_pokemon_profile(species_id)
        friendship = pokemon_data.get('friendship', 70)
        nature = pokemon_data.get('nature', 'Hardy')
        habitat = pokemon_data.get('habitat', 'unknown')
        
        # Get location traits for context
        location_traits = PokemonPersonalityBuilder._get_location_traits(habitat, species_id)
        
        # Base first encounter scenarios by intelligence level
        intelligence_reactions = {
            IntelligenceLevel.BASIC: {
                'confusion': "Where... where am I? This place smells strange...",
                'fear': "*looks around frantically, body tense and ready to flee*",
                'curiosity': "*sniffs the air cautiously, ears/senses alert*"
            },
            IntelligenceLevel.AVERAGE: {
                'confusion': "This isn't... this isn't where I was before. What happened to me?",
                'fear': "*backs away from the trainer, eyes darting for escape routes*",
                'curiosity': "*tilts head, studying the new environment with growing interest*"
            },
            IntelligenceLevel.HIGH: {
                'confusion': "I remember being in my territory, and now... I'm here. How did this happen?",
                'fear': "*maintains defensive posture while analyzing potential threats*",
                'curiosity': "*observes the trainer intently, trying to understand their intentions*"
            },
            IntelligenceLevel.GENIUS: {
                'confusion': "This is not my natural habitat. The displacement suggests capture and transport...",
                'fear': "*calculates escape possibilities while watching for aggressive moves*",
                'curiosity': "*studies the trainer with intelligent eyes, assessing their character*"
            },
            IntelligenceLevel.PSYCHIC: {
                'confusion': "The fabric of reality has shifted around me. I sense... digital constructs?",
                'fear': "*extends psychic senses, probing for threats in this strange realm*",
                'curiosity': "*reaches out telepathically, trying to understand this new existence*"
            }
        }
        
        intelligence = intelligence_profile['intelligence']
        base_reaction = intelligence_reactions.get(intelligence, intelligence_reactions[IntelligenceLevel.AVERAGE])
        
        # Modify based on nature and friendship
        nature_modifiers = {
            'Brave': {'fear_reduction': 0.3, 'curiosity_boost': 0.2},
            'Timid': {'fear_boost': 0.4, 'confusion_boost': 0.2},
            'Bold': {'fear_reduction': 0.4, 'curiosity_boost': 0.3},
            'Careful': {'confusion_boost': 0.2, 'fear_boost': 0.1},
            'Jolly': {'curiosity_boost': 0.3, 'fear_reduction': 0.1},
            'Lonely': {'confusion_boost': 0.3, 'fear_boost': 0.2},
            'Adamant': {'fear_reduction': 0.2, 'curiosity_boost': 0.1},
            'Docile': {'fear_boost': 0.1, 'confusion_boost': 0.1}
        }
        
        # Get habitat-specific memories that make the displacement more jarring
        habitat_displacement = {
            'forest': f"I remember the scent of pine needles and earth... now everything smells artificial.",
            'cave': f"The echo of my own voice in stone chambers... this silence feels wrong.",
            'waters-edge': f"The sound of flowing water, the feel of mud between my toes... where has it gone?",
            'mountain': f"The thin air and endless views from my peak... this enclosed space feels suffocating.",
            'grassland': f"Wind through the grass, the warmth of sun on my back... this place has no sky.",
            'urban': f"The familiar sounds of human activity... but this digital hum is different, strange."
        }
        
        displacement_memory = habitat_displacement.get(habitat, 
            "I remember... somewhere else. Somewhere that felt like home.")
        
        # Generate friendship-influenced first reaction
        if friendship < 50:  # Very low - recently caught, traumatic
            primary_emotion = 'fear'
            reaction_intensity = 'high'
            trust_level = 'none'
            opening_line = "Stay back! I don't know you, I don't know this place!"
        elif friendship < 100:  # Low but not traumatic
            primary_emotion = 'confusion'
            reaction_intensity = 'medium'
            trust_level = 'minimal'
            opening_line = "I... where am I? You're not the one who caught me..."
        else:  # Higher friendship - less traumatic awakening
            primary_emotion = 'curiosity'
            reaction_intensity = 'low'
            trust_level = 'cautious'
            opening_line = "This place is strange, but... you seem familiar somehow."
        
        return {
            'scenario_type': 'first_encounter',
            'primary_emotion': primary_emotion,
            'reaction_intensity': reaction_intensity,
            'trust_level': trust_level,
            'opening_line': opening_line,
            'base_reactions': base_reaction,
            'displacement_memory': displacement_memory,
            'habitat_context': location_traits,
            'nature_influence': nature_modifiers.get(nature, {}),
            'awakening_description': f"*{pokemon_data.get('nickname', pokemon_data.get('species_name', 'Pokemon'))} materializes in the digital space, immediately sensing the displacement from their natural environment*"
        }