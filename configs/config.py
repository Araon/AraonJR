"""
Configuration module for the AraonJR Discord bot
"""
import os
import sys
from typing import Optional
from dotenv import load_dotenv

def get_env_var(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """Get an environment variable with validation."""
    value = os.getenv(key, default)
    if required and not value:
        print(f"Error: Required environment variable '{key}' is not set.")
        sys.exit(1)
    return value

def get_int_env_var(key: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
    """Get an integer environment variable with validation."""
    value = get_env_var(key, str(default) if default is not None else None, required)
    if value is not None:
        try:
            return int(value)
        except ValueError:
            print(f"Error: Environment variable '{key}' must be an integer.")
            sys.exit(1)
    return None

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = get_env_var('BOT_TOKEN', required=True)
PREFIX = get_env_var('PREFIX', ';')
OWNER_ID = get_int_env_var('OWNER_ID', 322346259371393054)

# Testing configuration
TESTING_GUILD_ID = get_int_env_var('TESTING_GUILD_ID', 0)

# Colors for embeds
EMBED_COLOR = 0x3498db  # Blue color

# Music configuration
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# Version info
VERSION = '2.0.0'

# Validate configuration
def validate_config():
    """Validate the configuration values."""
    if not BOT_TOKEN or len(BOT_TOKEN) < 50:
        print("Error: Invalid BOT_TOKEN provided.")
        sys.exit(1)
        
    if not PREFIX:
        print("Error: PREFIX cannot be empty.")
        sys.exit(1)
        
    if OWNER_ID <= 0:
        print("Error: Invalid OWNER_ID provided.")
        sys.exit(1)

# Run validation when module is imported
validate_config()
