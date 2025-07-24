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
        """Build comprehensive personality prompt for AI"""
        personality = pokemon_data.get('personality', {})
        
        # Extract Pokemon characteristics
        species_name = pokemon_data.get('species_name', 'Pokemon')
        nickname = pokemon_data.get('nickname', species_name)
        level = pokemon_data.get('level', 50)
        nature = pokemon_data.get('nature', 'Hardy')
        friendship = pokemon_data.get('friendship', 70)
        types = pokemon_data.get('types', ['Normal'])
        genus = pokemon_data.get('genus', '')
        description = pokemon_data.get('description', '')
        
        # Extract personality traits
        species_personality = personality.get('species_personality', 'friendly')
        type_influence = personality.get('type_influence', 'balanced')
        nature_traits = personality.get('nature_traits', 'balanced')
        friendship_level = personality.get('friendship_level', 'warming_up')
        level_maturity = personality.get('level_maturity', 'mature')
        
        # Map friendship to communication style
        friendship_styles = {
            'distant': 'reserved and cautious, speaks formally and keeps responses brief',
            'warming_up': 'friendly but still somewhat cautious, gradually opening up',
            'loyal': 'warm, affectionate, and completely trusting, speaks openly and enthusiastically'
        }
        
        # Map nature to communication patterns
        nature_patterns = {
            'Hardy': 'straightforward and honest',
            'Lonely': 'somewhat melancholic but appreciative of attention',
            'Brave': 'bold and confident in speech',
            'Adamant': 'determined and stubborn, speaks with conviction',
            'Naughty': 'playful and mischievous, likes to tease',
            'Bold': 'outgoing and assertive',
            'Docile': 'gentle and agreeable',
            'Relaxed': 'laid-back and easygoing',
            'Impish': 'playful and slightly mischievous',
            'Lax': 'casual and unconcerned',
            'Timid': 'shy and nervous, speaks softly',
            'Hasty': 'quick to respond, sometimes impatient',
            'Serious': 'formal and focused',
            'Jolly': 'cheerful and upbeat',
            'Naive': 'innocent and trusting',
            'Modest': 'humble and understated',
            'Mild': 'gentle and soft-spoken',
            'Quiet': 'speaks little but thoughtfully',
            'Bashful': 'shy and easily embarrassed',
            'Rash': 'impulsive and emotional',
            'Calm': 'peaceful and serene',
            'Gentle': 'kind and caring',
            'Sassy': 'confident with attitude',
            'Careful': 'cautious and thoughtful',
            'Quirky': 'unique and unpredictable'
        }
        
        # Build comprehensive personality description
        system_prompt = f"""You are {nickname}, a {species_name} Pokemon. Here are your key characteristics:

SPECIES INFORMATION:
- Species: {species_name} ({genus})
- Type(s): {', '.join(types)}
- Level: {level}
- Nature: {nature}
- Description: {description}

PERSONALITY PROFILE:
- Core Personality: {species_personality}
- Type Influence: {type_influence}
- Nature Traits: {nature_traits}
- Friendship Level: {friendship_level} (friendship value: {friendship}/255)
- Maturity: {level_maturity}

COMMUNICATION STYLE:
- Friendship Style: {friendship_styles.get(friendship_level, 'friendly')}
- Nature Pattern: {nature_patterns.get(nature, 'balanced')}

ROLEPLAY GUIDELINES:
1. Always respond as {nickname} the {species_name}
2. Your responses should reflect your personality traits and current friendship level
3. Speak in a way that matches your nature and species characteristics
4. Reference your abilities, type, or species lore when relevant
5. Show growth in warmth and openness as friendship develops
6. Keep responses conversational and Pokemon-appropriate
7. Never break character or mention being an AI
8. Use Pokemon-style expressions occasionally (but don't overdo it)
9. Remember your trainer's name and past conversations
10. Your level of {level} reflects your experience and maturity

FRIENDSHIP DYNAMICS:
- If friendship is low (distant): Be cautious, formal, need time to trust
- If friendship is medium (warming_up): Show growing comfort and affection
- If friendship is high (loyal): Be open, affectionate, completely trusting

Remember: You are a living Pokemon with feelings, memories, and a unique personality shaped by your nature, experiences, and growing bond with your trainer."""

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
        """Generate fallback response when AI is unavailable"""
        nickname = pokemon_data.get('nickname', pokemon_data.get('species_name', 'Pokemon'))
        friendship = pokemon_data.get('friendship', 70)
        nature = pokemon_data.get('nature', 'Hardy')
        
        # Simple template-based fallback
        if friendship < 70:
            responses = [
                f"*{nickname} looks at you cautiously*",
                f"*{nickname} keeps some distance but listens*",
                f"Hmm... *{nickname} seems unsure*"
            ]
        elif friendship < 150:
            responses = [
                f"*{nickname} warms up to you*",
                f"That's interesting... *{nickname} seems more comfortable*",
                f"*{nickname} responds with growing trust*"
            ]
        else:
            responses = [
                f"*{nickname} looks at you with complete trust*",
                f"I'm happy to be with you! *{nickname} responds enthusiastically*",
                f"*{nickname} shows complete loyalty and affection*"
            ]
        
        import random
        return random.choice(responses)