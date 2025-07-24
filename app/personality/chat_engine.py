import random
import logging
from typing import Dict, List
from app.services.ai_chat_service import AIChatService

logger = logging.getLogger(__name__)

class ChatEngine:
    """Enhanced Pokemon personality-based chat response engine with AI integration"""
    
    def __init__(self):
        self.response_templates = self._load_response_templates()
        self.conversation_context = {}
        
        # Initialize AI service for dynamic responses
        self.ai_service = AIChatService()
        
        logger.info(f"Chat engine initialized. AI available: {self.ai_service.is_available()}")
        if self.ai_service.is_available():
            logger.info(f"Available AI providers: {[p.value for p in self.ai_service.available_providers]}")
    
    def generate_response(self, pokemon_data: Dict, user_message: str, conversation_history: List = None) -> str:
        """Generate a personality-appropriate response using AI or templates"""
        
        # Check if this is the first conversation (no previous messages)
        is_first_encounter = not conversation_history or len(conversation_history) == 0
        
        # Handle first encounter specially
        if is_first_encounter:
            return self._handle_first_encounter(pokemon_data, user_message)
        
        # Try AI-powered response first if available
        if self.ai_service.is_available():
            try:
                ai_response = self.ai_service.generate_pokemon_response(
                    user_message, pokemon_data, conversation_history
                )
                if ai_response and len(ai_response.strip()) > 0:
                    logger.info(f"Generated AI response for {pokemon_data.get('nickname', 'Pokemon')}")
                    return ai_response
            except Exception as e:
                logger.error(f"AI response generation failed: {e}")
        
        # Fallback to template-based responses
        logger.info(f"Using template-based response for {pokemon_data.get('nickname', 'Pokemon')}")
        return self._generate_template_response(pokemon_data, user_message, conversation_history)
    
    def _generate_template_response(self, pokemon_data: Dict, user_message: str, conversation_history: List = None) -> str:
        """Generate template-based response (original logic)"""
        personality = pokemon_data.get('personality', {})
        
        # Analyze user message for context
        message_type = self._analyze_message_type(user_message.lower())
        
        # Select appropriate response template based on personality and message type
        response_template = self._select_response_template(personality, message_type)
        
        # Generate personalized response
        response = self._personalize_response(response_template, pokemon_data, user_message)
        
        return response
    
    def _load_response_templates(self) -> Dict:
        """Load response templates organized by personality traits and message types"""
        return {
            'greeting': {
                'energetic': [
                    "Hey there! I'm so excited to talk with you!",
                    "Hi! What's up? I've been waiting to chat!",
                    "Hello! Ready for some fun conversation?"
                ],
                'gentle': [
                    "Hello there, friend. It's nice to meet you.",
                    "Hi! I hope you're having a wonderful day.",
                    "Greetings! I'm happy to chat with you."
                ],
                'confident': [
                    "Greetings. I suppose you want to talk?",
                    "Hello. I trust you have something interesting to say.",
                    "You have my attention. Speak."
                ],
                'playful': [
                    "Hehe! Hi there! Want to play or chat?",
                    "Hello! Got any fun stories to share?",
                    "Hi! What kind of mischief are we getting into today?"
                ],
                'mysterious': [
                    "So... you've come to speak with me.",
                    "Hello there. What brings you to me?",
                    "Interesting... another conversation begins."
                ],
                'shy': [
                    "Oh! H-hello there...",
                    "Um, hi... nice to meet you...",
                    "Hello... I hope we can be friends..."
                ]
            },
            'general': {
                'energetic': [
                    "That sounds amazing! Tell me more!",
                    "Wow! I love your enthusiasm!",
                    "That's so cool! What else is on your mind?"
                ],
                'gentle': [
                    "That's very interesting. How do you feel about it?",
                    "I appreciate you sharing that with me.",
                    "That sounds meaningful to you."
                ],
                'confident': [
                    "Naturally. I would expect nothing less.",
                    "Of course. That makes perfect sense.",
                    "An obvious conclusion, but well stated."
                ],
                'playful': [
                    "Ooh, that's fun! What happens next?",
                    "Hehe, I like the way you think!",
                    "That's amusing! Got any more stories?"
                ],
                'mysterious': [
                    "How intriguing... there's more to this, isn't there?",
                    "I see... the truth runs deeper than appearances.",
                    "Hmm... interesting perspective you have there."
                ],
                'shy': [
                    "Oh, that's... that's really nice...",
                    "I think I understand... maybe...",
                    "Um, that sounds important to you..."
                ]
            },
            'compliment': {
                'energetic': [
                    "Aww, thank you! You're pretty awesome too!",
                    "That's so sweet! You just made my day!",
                    "Thanks! You're the best!"
                ],
                'gentle': [
                    "Thank you so much. Your kindness means a lot to me.",
                    "That's very thoughtful of you to say.",
                    "I'm touched by your words. Thank you."
                ],
                'confident': [
                    "Well, of course I am. But thank you for noticing.",
                    "Your observation is correct. I appreciate the recognition.",
                    "Naturally. I'm glad you can see that."
                ],
                'playful': [
                    "Hehe, you flatter me! Want to be best friends?",
                    "Aww, you're making me blush! You're pretty great too!",
                    "Thanks! I think you're pretty special yourself!"
                ],
                'mysterious': [
                    "Your words... they reveal more about you than you know.",
                    "Interesting... few see me as I truly am.",
                    "Thank you... though I wonder what you truly see in me."
                ],
                'shy': [
                    "Oh! Um... th-thank you... that means a lot...",
                    "Really? You think so? That's... that's so nice...",
                    "I... I don't know what to say... thank you..."
                ]
            },
            'question': {
                'energetic': [
                    "Great question! Let me think... Well, I'd say...",
                    "Ooh! I love questions! Here's what I think:",
                    "That's a fun one to think about!"
                ],
                'gentle': [
                    "That's a thoughtful question. I believe...",
                    "Let me consider that carefully...",
                    "What a wonderful thing to ask about."
                ],
                'confident': [
                    "Obviously, the answer is...",
                    "I'm glad you asked. The truth is...",
                    "An excellent question with a clear answer:"
                ],
                'playful': [
                    "Ooh, you're curious! I like that! So...",
                    "Hehe, good question! Want to know a secret?",
                    "That's a fun mystery to solve!"
                ],
                'mysterious': [
                    "Ah... you ask the right questions...",
                    "Some answers are not easily given...",
                    "You seek knowledge... interesting..."
                ],
                'shy': [
                    "Oh, um... that's a good question... I think...",
                    "Well... if I had to guess... maybe...",
                    "That's... that's hard to answer... but maybe..."
                ]
            }
        }
    
    def _analyze_message_type(self, message: str) -> str:
        """Analyze user message to determine response type needed"""
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']
        compliments = ['amazing', 'awesome', 'great', 'wonderful', 'beautiful', 'cool', 'nice', 'good']
        questions = ['?', 'what', 'why', 'how', 'when', 'where', 'who', 'which', 'do you', 'are you', 'can you']
        
        if any(greeting in message for greeting in greetings):
            return 'greeting'
        elif any(compliment in message for compliment in compliments):
            return 'compliment'
        elif any(question in message for question in questions):
            return 'question'
        else:
            return 'general'
    
    def _select_response_template(self, personality: Dict, message_type: str) -> str:
        """Select appropriate response template based on personality"""
        # Determine primary personality trait
        primary_trait = self._get_primary_personality_trait(personality)
        
        # Get templates for message type and personality
        templates = self.response_templates.get(message_type, {})
        trait_templates = templates.get(primary_trait, templates.get('general', ['I understand.']))
        
        # Select random template
        return random.choice(trait_templates)
    
    def _get_primary_personality_trait(self, personality: Dict) -> str:
        """Determine primary personality trait from Pokemon data"""
        # Priority order for personality traits
        if personality.get('species_personality') == 'energetic':
            return 'energetic'
        elif personality.get('species_personality') == 'gentle':
            return 'gentle'
        elif personality.get('species_personality') == 'confident':
            return 'confident'
        elif personality.get('species_personality') == 'playful':
            return 'playful'
        elif personality.get('type_influence') == 'mysterious':
            return 'mysterious'
        elif personality.get('nature_traits') == 'shy':
            return 'shy'
        elif personality.get('type_influence') == 'energetic':
            return 'energetic'
        elif personality.get('nature_traits') == 'determined':
            return 'confident'
        else:
            return 'gentle'  # Default fallback
    
    def _personalize_response(self, template: str, pokemon_data: Dict, user_message: str) -> str:
        """Add personal touches to response based on Pokemon data"""
        response = template
        
        # Add friendship-based modifications
        friendship_level = pokemon_data.get('friendship', 0)
        if friendship_level < 70:
            # Distant responses
            response = self._make_response_distant(response)
        elif friendship_level > 150:
            # Affectionate responses
            response = self._make_response_affectionate(response, pokemon_data.get('nickname', 'friend'))
        
        # Add level-based maturity
        level = pokemon_data.get('level', 1)
        if level < 25:
            response = self._make_response_young(response)
        elif level > 50:
            response = self._make_response_wise(response)
        
        return response
    
    def _make_response_distant(self, response: str) -> str:
        """Make response more formal/distant for low friendship"""
        distant_modifiers = [
            lambda r: r.replace("!", "."),
            lambda r: r.replace("you're", "you are"),
            lambda r: r.replace("That's", "That is"),
            lambda r: r.replace("I'm", "I am")
        ]
        
        for modifier in distant_modifiers:
            response = modifier(response)
        
        return response
    
    def _make_response_affectionate(self, response: str, nickname: str) -> str:
        """Make response more affectionate for high friendship"""
        # Occasionally add affectionate terms
        if random.random() < 0.3:
            terms = [f"my friend", f"buddy", f"pal"]
            term = random.choice(terms)
            if not response.endswith('!'):
                response += f", {term}!"
            else:
                response = response[:-1] + f", {term}!"
        
        return response
    
    def _make_response_young(self, response: str) -> str:
        """Make response sound younger/more naive"""
        young_modifiers = [
            lambda r: r.replace("That's amazing", "That's super cool"),
            lambda r: r.replace("interesting", "neat"),
            lambda r: r.replace("wonderful", "awesome")
        ]
        
        for modifier in young_modifiers:
            response = modifier(response)
        
        return response
    
    def _make_response_wise(self, response: str) -> str:
        """Make response sound more mature/wise"""
        if random.random() < 0.2:
            wise_additions = [
                " In my experience, this often leads to growth.",
                " I've learned much about this over the years.",
                " Time has taught me to appreciate such moments."
            ]
            response += random.choice(wise_additions)
        
        return response
    
    def _handle_first_encounter(self, pokemon_data: Dict, user_message: str) -> str:
        """Handle the very first conversation with a Pokemon - special encounter scenario"""
        from app.services.pokemon_intelligence import PokemonPersonalityBuilder
        
        # Generate first encounter scenario
        first_encounter = PokemonPersonalityBuilder.get_first_encounter_scenario(pokemon_data)
        
        # Try AI-powered first encounter if available
        if self.ai_service.is_available():
            try:
                # Build special first encounter prompt
                first_encounter_prompt = f"""
FIRST ENCOUNTER SCENARIO: This is your very first interaction with your trainer in this digital space.

{first_encounter['awakening_description']}

SCENARIO CONTEXT:
- Primary Emotion: {first_encounter['primary_emotion'].upper()}
- Reaction Intensity: {first_encounter['reaction_intensity'].upper()}
- Trust Level: {first_encounter['trust_level'].upper()}

DISPLACEMENT MEMORY: {first_encounter['displacement_memory']}

Your first words should reflect:
1. Confusion about being in a strange new environment
2. {first_encounter['primary_emotion'].title()} as your dominant emotion
3. Your species-specific intelligence level and communication style
4. Memory fragments of your natural habitat
5. Uncertainty about who this trainer is and what they want

Trainer's first message to you: "{user_message}"

Respond as {pokemon_data.get('nickname', pokemon_data.get('species_name', 'Pokemon'))} experiencing this jarring first moment of awareness in the digital space. Your response should feel authentically like a frightened/confused animal that has just gained the ability to speak."""
                
                # Generate AI response with first encounter context
                from app.services.ai_chat_service import AIProvider
                provider = AIProvider.OPENAI if self.ai_service.openai_api_key else AIProvider.CLAUDE
                ai_response = self.ai_service._call_ai_api(
                    provider,
                    self.ai_service._build_personality_prompt(pokemon_data),
                    first_encounter_prompt
                )
                
                if ai_response and len(ai_response.strip()) > 0:
                    logger.info(f"Generated AI first encounter for {pokemon_data.get('nickname', 'Pokemon')}")
                    return ai_response
                    
            except Exception as e:
                logger.error(f"AI first encounter generation failed: {e}")
        
        # Fallback to template-based first encounter
        logger.info(f"Using template-based first encounter for {pokemon_data.get('nickname', 'Pokemon')}")
        return self._generate_template_first_encounter(pokemon_data, first_encounter, user_message)
    
    def _generate_template_first_encounter(self, pokemon_data: Dict, first_encounter: Dict, user_message: str) -> str:
        """Generate template-based first encounter response"""
        nickname = pokemon_data.get('nickname', pokemon_data.get('species_name', 'Pokemon'))
        
        # Start with awakening description
        response_parts = [first_encounter['awakening_description']]
        
        # Add opening reaction
        response_parts.append(first_encounter['opening_line'])
        
        # Add displacement memory
        response_parts.append(first_encounter['displacement_memory'])
        
        # Add species-specific confusion based on intelligence
        species_id = pokemon_data.get('species_id', 0)
        if species_id in [150]:  # Mewtwo - high intelligence
            response_parts.append("This digital construct... it defies natural law. What manner of technology is this?")
        elif species_id in [25]:  # Pikachu - medium-high intelligence
            response_parts.append("The air tastes wrong, smells wrong... nothing here feels real. What happened to the world?")
        elif species_id in [810]:  # Grookey - average intelligence
            response_parts.append("Where are all the trees? Where are the sounds of the forest? I... I want to go home...")
        else:
            response_parts.append("This place... it's not home. Not safe. Not right.")
        
        # Add nature-influenced reaction to trainer
        nature = pokemon_data.get('nature', 'Hardy')
        friendship = pokemon_data.get('friendship', 70)
        
        if friendship < 50:
            if nature in ['Brave', 'Bold', 'Adamant']:
                response_parts.append("*bristles defensively* Stay back! I don't know what you want, but I won't go down without a fight!")
            elif nature in ['Timid', 'Bashful', 'Careful']:
                response_parts.append("*cowers and trembles* P-please don't hurt me... I just want to go home...")
            else:
                response_parts.append("*backs away cautiously* Who are you? What do you want from me?")
        elif friendship < 100:
            response_parts.append("You... you feel familiar somehow, but I can't remember. Are you... are you safe?")
        else:
            response_parts.append("There's something about you... something comforting. But this place... it still scares me.")
        
        return " ".join(response_parts)