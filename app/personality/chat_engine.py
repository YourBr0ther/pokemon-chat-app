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
                    "*bounces excitedly, tail wagging* You're here! You smell familiar... trainer?",
                    "*perks up with bright eyes* Something new! *circles curiously* Are you safe?",
                    "*body vibrates with energy* This strange place feels less scary when you're here!"
                ],
                'gentle': [
                    "*approaches slowly with calm body language* Hello... you feel safe to me.",
                    "*tilts head with soft eyes* Your scent is kind. I sense no danger from you.",
                    "*settles peacefully nearby* In this strange place, your presence brings comfort."
                ],
                'confident': [
                    "*stands tall, assessing* You dare approach me in this realm? State your purpose.",
                    "*maintains steady gaze* I sense strength in you. What do you want, human?",
                    "*ears forward, alert but unafraid* You have earned my attention. Speak."
                ],
                'playful': [
                    "*pounces playfully* Ooh! A new friend! *spins in circle* Want to explore together?",
                    "*makes playful chittering sounds* You look fun! Got any games or adventures?",
                    "*wiggles with excitement* This digital place is weird, but you make it interesting!"
                ],
                'mysterious': [
                    "*emerges from shadows* So... you have found me in this strange realm.",
                    "*eyes glowing with ancient wisdom* Another soul wanders into my presence...",
                    "*voice echoes mysteriously* The digital winds brought you to me... interesting."
                ],
                'shy': [
                    "*hides partially, peeking out* Oh! *startled movements* H-hello... are you friendly?",
                    "*backs away cautiously* Um... *nervous body language* you won't hurt me, will you?",
                    "*whispers softly* Hello... *ready to flee* I'm still learning to trust here..."
                ]
            },
            'general': {
                'energetic': [
                    "*ears perk up, tail wagging faster* That sounds exciting! *bounces* Tell me more about this!",
                    "*eyes sparkle with interest* Wow! *spins around* Your energy makes me happy!",
                    "*vibrates with excitement* That's fascinating! *nose twitching* What else happened?"
                ],
                'gentle': [
                    "*listens attentively with soft eyes* That sounds important to you... *nods slowly*",
                    "*settles closer, showing trust* Thank you for sharing that with me, friend.",
                    "*tilts head thoughtfully* I can sense this means much to you..."
                ],
                'confident': [
                    "*nods with authority* Yes. This aligns with my understanding of things.",
                    "*maintains steady gaze* Of course. I expected as much from you.",
                    "*stands proudly* A sensible observation. You show wisdom."
                ],
                'playful': [
                    "*playful pounce* Ooh, that's interesting! *rolls over* What happened next?",
                    "*chittering with amusement* Hehe, I like how your mind works! *playful swat*",
                    "*wiggles excitedly* That sounds fun! *bounces* Got more stories like that?"
                ],
                'mysterious': [
                    "*eyes narrow with ancient knowledge* Intriguing... I sense deeper currents here...",
                    "*voice carries otherworldly wisdom* Yes... the surface hides greater truths...",
                    "*gazes into distance* Hmm... your words echo with hidden meaning..."
                ],
                'shy': [
                    "*peeks out shyly* Oh... *nervous fidgeting* that sounds really nice...",
                    "*whispers softly* I think... I think I understand... *hides partially*",
                    "*timid movements* Um... *quiet voice* that seems important to you..."
                ]
            },
            'compliment': {
                'energetic': [
                    "*tail wagging intensely* Aww! *bounces happily* You're amazing too, trainer!",
                    "*spins with joy* That makes my heart feel so warm! *nuzzles affectionately*",
                    "*beaming with happiness* Thanks! *playful hop* You make me feel special!"
                ],
                'gentle': [
                    "*soft purring sounds* Thank you... *rubs against you gently* Your kindness touches my soul.",
                    "*peaceful expression* Your words are like gentle sunlight... *settles contentedly*",
                    "*quiet gratitude* I'm deeply moved... *shows trust through relaxed posture*"
                ],
                'confident': [
                    "*stands with pride* Of course. You recognize quality when you see it.",
                    "*nods regally* Your judgment is sound. I am indeed impressive.",
                    "*chest puffed with dignity* Naturally. Few understand my true worth."
                ],
                'playful': [
                    "*rolls over giggling* Hehe, you make me happy! *paws playfully* Best friends forever?",
                    "*wiggles with delight* Aww, you're making me all fuzzy inside! *playful tackle*",
                    "*bounces excitedly* Thanks! *spins* I think you're absolutely wonderful too!"
                ],
                'mysterious': [
                    "*ancient eyes glowing* Your words... they carry deeper meaning than you know...",
                    "*voice echoes with wisdom* Few mortals perceive my true essence... interesting...",
                    "*gazes through dimensions* Thank you... though you see only shadows of what I am..."
                ],
                'shy': [
                    "*hides face, peeking through paws* Oh! *nervous giggling* Th-thank you so much...",
                    "*whispers with wonder* Really? You think so? *timid but happy movements*",
                    "*barely audible* I... I don't know what to say... *overwhelmed with joy*"
                ]
            },
            'question': {
                'energetic': [
                    "*ears perk up with curiosity* Ooh! *head tilts* Let me think with my animal brain... *excited pacing*",
                    "*bounces with interest* I love when you're curious! *spins* Here's what my instincts tell me:",
                    "*vibrates with thought* That makes my mind work! *nose twitching* Fun to ponder!"
                ],
                'gentle': [
                    "*settles thoughtfully* That's a deep question... *quiet contemplation* From my heart, I feel...",
                    "*tilts head with wisdom* Let me search my animal understanding... *soft rumbling*",
                    "*peaceful expression* Such wonderful curiosity... *content sigh* I sense..."
                ],
                'confident': [
                    "*stands with authority* The answer is clear to one such as I...",
                    "*powerful gaze* You seek wisdom. I shall provide it:",
                    "*regal bearing* An excellent inquiry. My superior knowledge reveals..."
                ],
                'playful': [
                    "*pounces on the question* Ooh, you're so curious! *wiggles* I like that about you!",
                    "*rolls over with glee* Hehe, want to know what I think? *playful swat* It's fun!",
                    "*bounces excitedly* That's like a puzzle for my animal brain! *spins* Let me figure it out!"
                ],
                'mysterious': [
                    "*eyes glow with ancient knowledge* Ah... you ask what few dare to question...",
                    "*voice echoes from otherworldly realms* Some truths are hidden in shadow...",
                    "*gazes beyond reality* You seek forbidden knowledge... how intriguing..."
                ],
                'shy': [
                    "*peeks out nervously* Oh... *fidgets* that's hard to answer... *whispers* maybe...",
                    "*hides partially* Um... *quiet voice* I'm not sure... *timid attempt* but perhaps...",
                    "*nervous movements* That's... that's really hard... *barely audible* I think maybe..."
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
        """Make response more wary/untrusting for low friendship - authentic animal behavior"""
        # Add cautious body language and keep distance
        distant_modifiers = [
            lambda r: r.replace("!", "..."),  # Less enthusiastic
            lambda r: r.replace("*bounces excitedly*", "*keeps distance, watching*"),
            lambda r: r.replace("*approaches*", "*stays back, observing*"),
            lambda r: r.replace("*nuzzles*", "*sniffs cautiously from afar*"),
            lambda r: r.replace("trainer", "human"),  # More formal address
        ]
        
        for modifier in distant_modifiers:
            response = modifier(response)
        
        # Add wary animal behavior
        if "*" not in response:  # Only add if no body language already present
            response = "*ears back, maintaining distance* " + response
        
        return response
    
    def _make_response_affectionate(self, response: str, nickname: str) -> str:
        """Make response more bonded/trusting for high friendship - authentic animal behavior"""
        # Add close bonding behaviors
        affectionate_modifiers = [
            lambda r: r.replace("*approaches slowly*", "*bounds over eagerly*"),
            lambda r: r.replace("*keeps distance*", "*comes close, seeking comfort*"),
            lambda r: r.replace("human", "my trusted human"),
            lambda r: r.replace("you", "you, my bonded one") if random.random() < 0.2 else r,
        ]
        
        for modifier in affectionate_modifiers:
            response = modifier(response)
        
        # Add bonded animal behaviors
        if random.random() < 0.4:
            bonding_behaviors = [
                "*rubs against you affectionately*",
                "*nuzzles you with deep trust*", 
                "*settles close to your side*",
                "*purrs contentedly in your presence*"
            ]
            behavior = random.choice(bonding_behaviors)
            response += f" {behavior}"
        
        return response
    
    def _make_response_young(self, response: str) -> str:
        """Make response show youthful animal energy and curiosity"""
        young_modifiers = [
            lambda r: r.replace("*settles*", "*wiggles impatiently*"),
            lambda r: r.replace("*approaches*", "*bounds over playfully*"),
            lambda r: r.replace("*listens*", "*ears perked, practically vibrating with attention*"),
            lambda r: r.replace("I sense", "Ooh, I feel"),
            lambda r: r.replace("I understand", "I think I get it!"),
        ]
        
        for modifier in young_modifiers:
            response = modifier(response)
        
        # Add youthful animal behaviors
        if random.random() < 0.3:
            youthful_additions = [
                " *bounces with puppy-like enthusiasm*",
                " *spins in excited circles*", 
                " *paws at the ground with eager energy*",
                " *tilts head with innocent curiosity*"
            ]
            response += random.choice(youthful_additions)
        
        return response
    
    def _make_response_wise(self, response: str) -> str:
        """Make response show mature animal wisdom and experience"""
        wise_modifiers = [
            lambda r: r.replace("*bounces*", "*settles with dignified composure*"),
            lambda r: r.replace("*spins*", "*moves with measured grace*"),
            lambda r: r.replace("That's exciting!", "That holds deep meaning."),
        ]
        
        for modifier in wise_modifiers:
            response = modifier(response)
        
        # Add wise animal behaviors and insights
        if random.random() < 0.3:
            wise_additions = [
                " *gazes with the wisdom of many seasons*",
                " *nods with ancient understanding* I have seen much in my long life.",
                " *settles with the patience that comes from experience*",
                " My old bones have felt many such moments..."
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