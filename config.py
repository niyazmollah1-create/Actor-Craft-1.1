import os

# Bot configuration
BOT_CONFIG = {
    'prefix': '!',  # Fallback prefix for text commands (if any)
    'description': 'A multi-purpose Discord bot with utility, moderation, and fun commands',
    'case_insensitive': True,
    'strip_after_prefix': True,
    
    # Bot settings
    'max_messages': 1000,  # Max messages to cache
    'heartbeat_timeout': 60.0,
    
    # Command settings
    'command_timeout': 30.0,  # Timeout for commands in seconds
    
    # Embed colors (in hex)
    'colors': {
        'success': 0x00ff00,
        'error': 0xff0000,
        'warning': 0xffff00,
        'info': 0x0099ff,
        'default': 0x7289da
    },
    
    # API endpoints for fun commands
    'api_endpoints': {
        'jokes': 'https://official-joke-api.appspot.com/random_joke',
        'quotes': 'https://api.quotable.io/random',
        'facts': 'https://uselessfacts.jsph.pl/random.json?language=en'
    },
    
    # Rate limiting
    'rate_limits': {
        'per_user': 5,  # Commands per user per bucket
        'per_bucket': 10.0,  # Bucket duration in seconds
        'global_rate_limit': 100  # Global commands per minute
    },
    
    # Logging configuration
    'logging': {
        'level': 'INFO',
        'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        'file': 'bot.log',
        'max_bytes': 5 * 1024 * 1024,  # 5MB
        'backup_count': 3
    }
}

# Environment variables with defaults
def get_env_var(name: str, default=None, required: bool = False):
    """Get environment variable with optional default and requirement check"""
    value = os.getenv(name, default)
    if required and value is None:
        raise ValueError(f"Required environment variable {name} is not set")
    return value

# Required environment variables
REQUIRED_ENV_VARS = {
    'DISCORD_TOKEN': get_env_var('DISCORD_TOKEN', required=True)
}

# Optional environment variables
OPTIONAL_ENV_VARS = {
    'BOT_PREFIX': get_env_var('BOT_PREFIX', BOT_CONFIG['prefix']),
    'LOG_LEVEL': get_env_var('LOG_LEVEL', BOT_CONFIG['logging']['level']),
    'COMMAND_TIMEOUT': float(get_env_var('COMMAND_TIMEOUT', BOT_CONFIG['command_timeout']))
}

# Update config with environment variables
BOT_CONFIG['prefix'] = OPTIONAL_ENV_VARS['BOT_PREFIX']
BOT_CONFIG['logging']['level'] = OPTIONAL_ENV_VARS['LOG_LEVEL']
BOT_CONFIG['command_timeout'] = OPTIONAL_ENV_VARS['COMMAND_TIMEOUT']
