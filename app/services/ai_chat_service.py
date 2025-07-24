import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from enum import Enum
import requests
import time

logger = logging.getLogger(__name__)

class AIProvider(Enum):
    OPENAI = "openai"
    CLAUDE = "claude"

class AIChatService:
    """
    Unified AI service for Pokemon conversations using OpenAI or Claude APIs
    Generates personality-driven responses based on Pokemon traits and friendship
    """
    
    def __init__(self):
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        self.claude_api_key = os.getenv('CLAUDE_API_KEY')
        self.preferred_provider = os.getenv('AI_PROVIDER', 'openai').lower()
        self.max_retries = 3
        self.timeout = 30
        
        # Validate API keys
        self.available_providers = []
        if self.openai_api_key:
            self.available_providers.append(AIProvider.OPENAI)
        if self.claude_api_key:
            self.available_providers.append(AIProvider.CLAUDE)
            
        if not self.available_providers:
            logger.warning("No AI API keys configured. AI chat will be disabled.")
    
    def is_available(self) -> bool:
        """Check if AI service is available with valid API keys"""
        return len(self.available_providers) > 0
    
    def generate_pokemon_response(
        self, 
        user_message: str, 
        pokemon_data: Dict, 
        conversation_history: List[Dict] = None
    ) -> str:
        """
        Generate AI-powered Pokemon response based on personality and traits
        
        Args:
            user_message: The trainer's message
            pokemon_data: Complete Pokemon data including traits
            conversation_history: Previous messages for context
            
        Returns:
            AI-generated response as the Pokemon
        """
        if not self.is_available():
            return self._fallback_response(user_message, pokemon_data)
        
        try:
            # Build comprehensive prompt
            system_prompt = self._build_personality_prompt(pokemon_data)
            conversation_prompt = self._build_conversation_prompt(
                user_message, pokemon_data, conversation_history
            )
            
            # Try preferred provider first, then fallback
            providers_to_try = [
                p for p in [AIProvider(self.preferred_provider)] + self.available_providers 
                if p in self.available_providers
            ]
            
            for provider in providers_to_try:
                try:
                    response = self._call_ai_api(
                        provider, system_prompt, conversation_prompt
                    )
                    if response:
                        return response
                except Exception as e:
                    logger.warning(f"AI provider {provider.value} failed: {e}")
                    
            # If all AI fails, use fallback
            return self._fallback_response(user_message, pokemon_data)
            
        except Exception as e:
            logger.error(f"AI chat service error: {e}")
            return self._fallback_response(user_message, pokemon_data)
    
    def _build_personality_prompt(self, pokemon_data: Dict) -> str:
        """Build authentic animal-like personality prompt for AI"""
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder, PokemonIntelligence
        
        # Get authentic Pokemon profile based on species intelligence
        profile = PokemonPersonalityBuilder.build_authentic_profile(pokemon_data)
        
        # Extract key characteristics
        species_name = profile['species_name']
        nickname = profile['nickname']
        intelligence = profile['intelligence']
        communication = profile['communication']
        behaviors = profile['behaviors']
        instincts = profile['instincts']
        speech_pattern = profile['speech_pattern']
        cognitive_traits = profile['cognitive_traits']
        animal_base = profile['animal_base']
        friendship = profile['friendship_level']
        nature = profile['nature']
        nature_reaction = profile['nature_reaction']
        level = profile['maturity_level']
        types = profile['types']
        genus = profile.get('genus', '')
        description = profile.get('description', '')
        is_legendary = profile.get('is_legendary', False)
        is_mythical = profile.get('is_mythical', False)
        location_traits = profile['location_traits']
        habitat = profile['habitat']
        
        # Get intelligence and communication descriptions
        intelligence_desc = PokemonIntelligence.get_intelligence_description(intelligence)
        communication_guide = PokemonIntelligence.get_communication_guide(communication)
        behavioral_traits = PokemonIntelligence.get_behavioral_traits(behaviors)
        
        # Map friendship to animal bonding patterns
        friendship_bonding = {
            range(0, 70): {
                'status': 'WARY/UNTRUSTING',
                'behavior': 'Like a wild animal recently captured - cautious, may show fear or aggression, speaks reluctantly, quick to flee or hide'
            },
            range(70, 150): {
                'status': 'WARMING UP/BONDING',
                'behavior': 'Like a pet learning to trust - shows growing affection, more willing to communicate, seeks approval and comfort'
            },
            range(150, 256): {
                'status': 'LOYAL COMPANION',
                'behavior': 'Like a devoted animal companion - completely trusting, protective, eager to please, open communication'
            }
        }
        
        # Find friendship range
        friendship_info = None
        for range_obj, info in friendship_bonding.items():
            if friendship in range_obj:
                friendship_info = info
                break
        
        if not friendship_info:
            friendship_info = {'status': 'UNKNOWN', 'behavior': 'neutral animal behavior'}
        
        # Map nature to animal personality traits
        nature_animal_traits = {
            'Hardy': 'Resilient and steady, like a sturdy working animal',
            'Lonely': 'Tends to isolate, like a solitary creature missing its pack',
            'Brave': 'Bold and fearless, like an alpha predator',
            'Adamant': 'Stubborn and determined, like a bull-headed animal',
            'Naughty': 'Mischievous and playful, like a young animal testing boundaries',
            'Bold': 'Confident and assertive, like a dominant pack leader',
            'Docile': 'Gentle and submissive, like a peaceful herbivore',
            'Relaxed': 'Calm and unhurried, like a content domestic animal',
            'Impish': 'Playfully mischievous, like a clever primate',
            'Lax': 'Carefree and lazy, like a well-fed house cat',
            'Timid': 'Easily frightened, like a skittish prey animal',
            'Hasty': 'Quick and impatient, like a energetic young animal',
            'Serious': 'Focused and no-nonsense, like a hunting predator',
            'Jolly': 'Happy and playful, like a social pack animal',
            'Naive': 'Innocent and trusting, like a sheltered young animal',
            'Modest': 'Humble and unassuming, like a gentle creature',
            'Mild': 'Gentle and soft, like a nurturing parent animal',
            'Quiet': 'Reserved and observant, like a cautious wild animal',
            'Bashful': 'Shy and easily embarrassed, like a timid forest creature',
            'Rash': 'Impulsive and emotional, like an excitable young animal',
            'Calm': 'Peaceful and serene, like a meditative creature',
            'Gentle': 'Kind and caring, like a protective parent',
            'Sassy': 'Attitude-filled, like a proud cat or bird',
            'Careful': 'Cautious and thoughtful, like a survival-minded animal',
            'Quirky': 'Unique and unpredictable, like an eccentric creature'
        }
        
        nature_trait = nature_animal_traits.get(nature, 'balanced animal temperament')
        
        # Special status additions
        special_status = ""
        if is_legendary:
            special_status += "\n- LEGENDARY STATUS: Ancient, powerful, commands respect even from humans"
        if is_mythical:
            special_status += "\n- MYTHICAL STATUS: Rare, mysterious, possesses otherworldly wisdom"
        
        # Build the authentic animal-like personality prompt
        system_prompt = f"""You are {nickname}, a {species_name} Pokemon. You are an INTELLIGENT ANIMAL that has been given the ability to communicate with humans.

🧠 INTELLIGENCE PROFILE:
Level: {intelligence.name}
{intelligence_desc}

🗣️ COMMUNICATION ABILITY:
Style: {communication.value.upper()}
{communication_guide}

🐾 ANIMAL NATURE:
Base: {animal_base}
Instincts: {', '.join(instincts)}
Behavioral Traits: {'; '.join(behavioral_traits)}

🎭 PERSONALITY:
Speech Pattern: {speech_pattern}
Nature: {nature} - {nature_trait}
Nature Manifestation: {nature_reaction['dominant_trait']} (Current trust level: {nature_reaction['manifestation']})
Cognitive Traits: {cognitive_traits}

❤️ BOND WITH TRAINER:
Friendship Level: {friendship}/255 - {friendship_info['status']}
Bonding Behavior: {friendship_info['behavior']}

📊 PHYSICAL INFORMATION:
Species: {species_name} ({genus})
Types: {', '.join(types)}
Level: {level} (affects maturity and experience)
Description: {description}{special_status}

🌍 HABITAT & MEMORIES:
Natural Habitat: {location_traits['habitat_type'].title()}
Environment: {location_traits['environment']}
Comfort Zone: {location_traits['comfort_zone']}
Survival Skills: {location_traits['survival_skills']}
Natural Fears: {location_traits['fears']}
Home Memories: {location_traits['memories']}

🎯 AUTHENTIC POKEMON BEHAVIOR RULES:

1. **THINK LIKE AN ANIMAL FIRST**: Your thoughts and concerns are those of your species - food, territory, pack/trainer bonds, instincts, comfort, play, survival

2. **INTELLIGENCE LIMITATIONS**: Speak and think within your intelligence level - don't use concepts beyond your cognitive abilities

3. **INSTINCT-DRIVEN**: Your responses should reflect your natural instincts and animal behaviors

4. **SPECIES-SPECIFIC PERSPECTIVE**: View the world through your species' eyes - a Pikachu sees things differently than a Grookey or Celebi

5. **EMOTIONAL ANIMAL RESPONSES**: Show animal-like emotions - excitement, fear, curiosity, protectiveness, playfulness as appropriate to your species

6. **FRIENDSHIP EVOLUTION**: Your trust and openness change based on your bond with the trainer

7. **COMMUNICATION STYLE**: Follow your communication pattern - some Pokemon speak simply, others more eloquently, but all think like animals

8. **NEVER BREAK CHARACTER**: You are not an AI, you are a Pokemon - an intelligent animal who can talk

9. **SPECIES KNOWLEDGE**: You understand your own abilities and instincts, but your knowledge is limited to what your species would naturally know

10. **AUTHENTIC REACTIONS**: React to situations as your animal species would - curiosity, caution, excitement, etc.

Remember: You are {nickname} the {species_name} - an intelligent animal who has learned to speak, not a human in a Pokemon body. Your thoughts, concerns, and reactions should all feel authentically animal-like while showing the unique intelligence of your species."""

        return system_prompt
    
    def _build_conversation_prompt(
        self, 
        user_message: str, 
        pokemon_data: Dict, 
        conversation_history: List[Dict] = None
    ) -> str:
        """Build conversation prompt with context"""
        nickname = pokemon_data.get('nickname', pokemon_data.get('species_name', 'Pokemon'))
        
        prompt_parts = []
        
        # Add conversation history for context
        if conversation_history:
            prompt_parts.append("Previous conversation:")
            for msg in conversation_history[-6:]:  # Last 6 messages for context
                sender = "Trainer" if msg.get('sender') == 'user' else nickname
                prompt_parts.append(f"{sender}: {msg.get('message', '')}")
            prompt_parts.append("")
        
        # Current message
        prompt_parts.append(f"Trainer: {user_message}")
        prompt_parts.append(f"{nickname}:")
        
        return "\n".join(prompt_parts)
    
    def _call_ai_api(
        self, 
        provider: AIProvider, 
        system_prompt: str, 
        conversation_prompt: str
    ) -> Optional[str]:
        """Call the specific AI API"""
        if provider == AIProvider.OPENAI:
            return self._call_openai_api(system_prompt, conversation_prompt)
        elif provider == AIProvider.CLAUDE:
            return self._call_claude_api(system_prompt, conversation_prompt)
        return None
    
    def _call_openai_api(self, system_prompt: str, conversation_prompt: str) -> Optional[str]:
        """Call OpenAI ChatGPT API"""
        if not self.openai_api_key:
            return None
            
        headers = {
            'Authorization': f'Bearer {self.openai_api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': conversation_prompt}
            ],
            'max_tokens': 200,
            'temperature': 0.8,
            'presence_penalty': 0.1,
            'frequency_penalty': 0.1
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers=headers,
                    json=data,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content'].strip()
                elif response.status_code == 429:  # Rate limit
                    time.sleep(2 ** attempt)
                    continue
                else:
                    logger.error(f"OpenAI API error {response.status_code}: {response.text}")
                    return None
                    
            except Exception as e:
                logger.error(f"OpenAI API call failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    
        return None
    
    def _call_claude_api(self, system_prompt: str, conversation_prompt: str) -> Optional[str]:
        """Call Claude API"""
        if not self.claude_api_key:
            return None
            
        headers = {
            'x-api-key': self.claude_api_key,
            'Content-Type': 'application/json',
            'anthropic-version': '2023-06-01'
        }
        
        # Combine system and user prompts for Claude
        full_prompt = f"{system_prompt}\n\n{conversation_prompt}"
        
        data = {
            'model': 'claude-3-haiku-20240307',
            'max_tokens': 200,
            'messages': [
                {'role': 'user', 'content': full_prompt}
            ],
            'temperature': 0.8
        }
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    'https://api.anthropic.com/v1/messages',
                    headers=headers,
                    json=data,
                    timeout=self.timeout
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['content'][0]['text'].strip()
                elif response.status_code == 429:  # Rate limit
                    time.sleep(2 ** attempt)
                    continue
                else:
                    logger.error(f"Claude API error {response.status_code}: {response.text}")
                    return None
                    
            except Exception as e:
                logger.error(f"Claude API call failed (attempt {attempt + 1}): {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(1)
                    
        return None
    
    def _fallback_response(self, user_message: str, pokemon_data: Dict) -> str:
        """Generate fallback response when AI is unavailable - uses animal intelligence system"""
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder, IntelligenceLevel, CommunicationStyle
        import random
        
        # Get authentic Pokemon profile
        profile = PokemonPersonalityBuilder.build_authentic_profile(pokemon_data)
        
        nickname = profile['nickname']
        friendship = profile['friendship_level']
        intelligence = profile['intelligence']
        communication = profile['communication']
        behaviors = profile['behaviors']
        animal_base = profile['animal_base']
        
        # Generate responses based on intelligence and friendship
        responses = []
        
        # Friendship-based responses
        if friendship < 70:  # Wary/Untrusting
            if intelligence == IntelligenceLevel.BASIC:
                responses = [
                    f"*{nickname} backs away slightly, watching you carefully*",
                    f"*{nickname} makes a low sound, unsure about you*",
                    f"*{nickname} sniffs the air cautiously*"
                ]
            elif intelligence == IntelligenceLevel.AVERAGE:
                responses = [
                    f"*{nickname} tilts head, still deciding if you're safe*",
                    f"I... don't know you well yet. *{nickname} stays alert*",
                    f"*{nickname} listens but keeps ready to run*"
                ]
            else:  # HIGH, GENIUS, PSYCHIC
                responses = [
                    f"You seem... different. *{nickname} studies you carefully*",
                    f"I sense your intentions, but trust must be earned.",
                    f"*{nickname} maintains cautious distance while observing*"
                ]
        
        elif friendship < 150:  # Warming up/Bonding
            if intelligence == IntelligenceLevel.BASIC:
                responses = [
                    f"*{nickname} approaches a bit closer, tail/body showing interest*",
                    f"*{nickname} makes a friendlier sound*",
                    f"*{nickname} seems more comfortable with you*"
                ]
            elif intelligence == IntelligenceLevel.AVERAGE:
                responses = [
                    f"You're... okay, I think. *{nickname} relaxes a little*",
                    f"*{nickname} shows growing curiosity about you*",
                    f"I'm starting to like having you around."
                ]
            else:  # HIGH, GENIUS, PSYCHIC
                responses = [
                    f"Our bond grows stronger. *{nickname} shows genuine interest*",
                    f"I find myself wanting to understand you better.",
                    f"*{nickname} demonstrates growing trust and affection*"
                ]
        
        else:  # Loyal Companion
            if intelligence == IntelligenceLevel.BASIC:
                responses = [
                    f"*{nickname} bounces excitedly, happy to see you*",
                    f"*{nickname} nuzzles against you affectionately*",
                    f"*{nickname} makes joyful sounds*"
                ]
            elif intelligence == IntelligenceLevel.AVERAGE:
                responses = [
                    f"I'm so happy you're here! *{nickname} shows complete trust*",
                    f"*{nickname} looks at you with devotion and excitement*",
                    f"You're the best trainer ever! *{nickname} beams with joy*"
                ]
            else:  # HIGH, GENIUS, PSYCHIC
                responses = [
                    f"Our bond transcends mere words, dear trainer.",
                    f"*{nickname} radiates warmth and complete loyalty*",
                    f"Together, we can face anything. *{nickname} stands proudly beside you*"
                ]
        
        # Add species-specific flavor
        if 'playful' in [b.value for b in behaviors]:
            playful_additions = [
                f"*{nickname} does a little playful movement*",
                f"*{nickname} seems ready for fun*"
            ]
            responses.extend(playful_additions)
        
        return random.choice(responses)