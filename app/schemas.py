"""
Input validation schemas for API endpoints
"""
from marshmallow import Schema, fields, validate, ValidationError
import re

class PokemonSaveSchema(Schema):
    """Schema for validating Pokemon save data"""
    species = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    nickname = fields.Str(required=False, allow_none=True, validate=validate.Length(max=12))
    level = fields.Int(required=True, validate=validate.Range(min=1, max=100))
    nature = fields.Str(required=True, validate=validate.Length(min=1, max=20))
    ability = fields.Str(required=True, validate=validate.Length(min=1, max=30))
    friendship = fields.Int(required=True, validate=validate.Range(min=0, max=255))
    iv_hp = fields.Int(required=True, validate=validate.Range(min=0, max=31))
    iv_attack = fields.Int(required=True, validate=validate.Range(min=0, max=31))
    iv_defense = fields.Int(required=True, validate=validate.Range(min=0, max=31))
    iv_sp_attack = fields.Int(required=True, validate=validate.Range(min=0, max=31))
    iv_sp_defense = fields.Int(required=True, validate=validate.Range(min=0, max=31))
    iv_speed = fields.Int(required=True, validate=validate.Range(min=0, max=31))
    is_shiny = fields.Bool(required=False, missing=False)
    gender = fields.Str(required=False, allow_none=True, validate=validate.OneOf(['M', 'F', None]))
    
    def validate_nickname(self, value):
        """Custom validation for nickname to prevent HTML/JS injection"""
        if value and re.search(r'[<>"\']', value):
            raise ValidationError("Nickname cannot contain HTML characters")
        return value

class ChatMessageSchema(Schema):
    """Schema for validating chat messages"""
    message = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    
    def validate_message(self, value):
        """Sanitize message content"""
        # Basic HTML tag detection
        if re.search(r'<[^>]*>', value):
            raise ValidationError("Message cannot contain HTML tags")
        return value

class TeamActionSchema(Schema):
    """Schema for team add/remove actions"""
    pokemon_id = fields.Int(required=True, validate=validate.Range(min=1))

class PokemonIdSchema(Schema):
    """Schema for Pokemon ID validation"""
    id = fields.Int(required=True, validate=validate.Range(min=1))

def validate_json_input(schema_class, json_data):
    """
    Helper function to validate JSON input against a schema
    
    Args:
        schema_class: Marshmallow schema class
        json_data: JSON data to validate
        
    Returns:
        tuple: (is_valid, validated_data_or_errors)
    """
    try:
        schema = schema_class()
        validated_data = schema.load(json_data)
        return True, validated_data
    except ValidationError as err:
        return False, err.messages

def sanitize_html_content(content):
    """
    Basic HTML sanitization for content
    
    Args:
        content: String content to sanitize
        
    Returns:
        str: Sanitized content
    """
    if not isinstance(content, str):
        return content
    
    # Remove common HTML tags and entities
    html_chars = {
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        '\'': '&#x27;',
        '&': '&amp;'
    }
    
    for char, entity in html_chars.items():
        content = content.replace(char, entity)
    
    return content