from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Pokemon(db.Model):
    """Pokemon model for storing imported Pokemon data"""
    __tablename__ = 'pokemon'
    
    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(db.Integer, nullable=False)
    species_name = db.Column(db.String(50), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    nature = db.Column(db.String(20), nullable=False)
    friendship = db.Column(db.Integer, nullable=False, default=0)
    types = db.Column(db.String(50), nullable=False)  # JSON string of types array
    original_trainer = db.Column(db.String(50), nullable=False)
    personality_hash = db.Column(db.Text)  # JSON string of personality traits
    ivs = db.Column(db.Text)  # JSON string of IV stats
    
    # PokeAPI enhanced data
    sprite_url = db.Column(db.String(255))  # Main sprite URL
    sprite_shiny_url = db.Column(db.String(255))  # Shiny variant
    official_artwork_url = db.Column(db.String(255))  # High-quality artwork
    description = db.Column(db.Text)  # Pokédex flavor text
    genus = db.Column(db.String(50))  # e.g., "Seed Pokémon"
    height = db.Column(db.Integer)  # Height in decimeters
    weight = db.Column(db.Integer)  # Weight in hectograms
    base_happiness = db.Column(db.Integer)  # Base happiness/friendship
    capture_rate = db.Column(db.Integer)  # How easy to catch
    is_legendary = db.Column(db.Boolean, default=False)
    is_mythical = db.Column(db.Boolean, default=False)
    habitat = db.Column(db.String(50))  # Natural habitat
    pokemon_color = db.Column(db.String(20))  # Primary color
    abilities = db.Column(db.Text)  # JSON string of abilities
    base_stats = db.Column(db.Text)  # JSON string of base stats
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    team_members = db.relationship('TeamMember', backref='pokemon', lazy=True, cascade='all, delete-orphan')
    chat_messages = db.relationship('ChatMessage', backref='pokemon', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def set_types(self, types_list):
        """Set types as JSON string"""
        self.types = json.dumps(types_list)
    
    def get_types(self):
        """Get types as list"""
        try:
            return json.loads(self.types)
        except:
            return ["Normal"]
    
    def set_personality(self, personality_dict):
        """Set personality traits as JSON string"""
        self.personality_hash = json.dumps(personality_dict)
    
    def get_personality(self):
        """Get personality traits as dictionary"""
        try:
            return json.loads(self.personality_hash)
        except:
            return {}
    
    def set_ivs(self, ivs_dict):
        """Set IVs as JSON string"""
        self.ivs = json.dumps(ivs_dict)
    
    def get_ivs(self):
        """Get IVs as dictionary"""
        try:
            return json.loads(self.ivs)
        except:
            return {'hp': 0, 'attack': 0, 'defense': 0, 'sp_attack': 0, 'sp_defense': 0, 'speed': 0}
    
    def set_abilities(self, abilities_list):
        """Set abilities as JSON string"""
        self.abilities = json.dumps(abilities_list)
    
    def get_abilities(self):
        """Get abilities as list"""
        try:
            return json.loads(self.abilities)
        except:
            return []
    
    def set_base_stats(self, stats_dict):
        """Set base stats as JSON string"""
        self.base_stats = json.dumps(stats_dict)
    
    def get_base_stats(self):
        """Get base stats as dictionary"""
        try:
            return json.loads(self.base_stats)
        except:
            return {}
    
    def get_height_formatted(self):
        """Get height in meters (from decimeters)"""
        if self.height:
            return f"{self.height / 10:.1f}m"
        return "Unknown"
    
    def get_weight_formatted(self):
        """Get weight in kg (from hectograms)"""
        if self.weight:
            return f"{self.weight / 10:.1f}kg"
        return "Unknown"
    
    def get_best_sprite(self):
        """Get the best available sprite URL"""
        return (self.official_artwork_url or 
                self.sprite_url or 
                f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{self.species_id}.png")
    
    def to_dict(self):
        """Convert Pokemon to dictionary"""
        return {
            'id': self.id,
            'species_id': self.species_id,
            'species_name': self.species_name,
            'nickname': self.nickname,
            'level': self.level,
            'nature': self.nature,
            'friendship': self.friendship,
            'types': self.get_types(),
            'original_trainer': self.original_trainer,
            'personality': self.get_personality(),
            'ivs': self.get_ivs(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            
            # PokeAPI enhanced data
            'sprite_url': self.sprite_url,
            'sprite_shiny_url': self.sprite_shiny_url,
            'official_artwork_url': self.official_artwork_url,
            'best_sprite': self.get_best_sprite(),
            'description': self.description,
            'genus': self.genus,
            'height': self.height,
            'weight': self.weight,
            'height_formatted': self.get_height_formatted(),
            'weight_formatted': self.get_weight_formatted(),
            'base_happiness': self.base_happiness,
            'capture_rate': self.capture_rate,
            'is_legendary': self.is_legendary,
            'is_mythical': self.is_mythical,
            'habitat': self.habitat or 'unknown',
            'pokemon_color': self.pokemon_color,
            'abilities': self.get_abilities(),
            'base_stats': self.get_base_stats()
        }

class TeamMember(db.Model):
    """Team composition model"""
    __tablename__ = 'team'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False, default='default_user')
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    slot_number = db.Column(db.Integer, nullable=False)  # 1-6
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'slot_number', name='unique_user_slot'),
        db.UniqueConstraint('user_id', 'pokemon_id', name='unique_user_pokemon'),
    )
    
    def to_dict(self):
        """Convert TeamMember to dictionary"""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'pokemon_id': self.pokemon_id,
            'slot_number': self.slot_number,
            'pokemon': self.pokemon.to_dict() if self.pokemon else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ChatMessage(db.Model):
    """Chat history model"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    sender = db.Column(db.String(10), nullable=False)  # 'user' or 'pokemon'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert ChatMessage to dictionary"""
        return {
            'id': self.id,
            'pokemon_id': self.pokemon_id,
            'message': self.message,
            'sender': self.sender,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'pokemon_nickname': self.pokemon.nickname if self.pokemon else None
        }