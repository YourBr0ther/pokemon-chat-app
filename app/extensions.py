"""
Flask extensions configuration
"""
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize limiter that can be imported by blueprints
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["1000 per hour", "100 per minute"],
    storage_uri="memory://"
)