#!/usr/bin/env python3
"""
Configuration Template for Telegram Monitor
Copy this file to config.py and fill in your actual values
"""

# =============================================================================
# TELEGRAM API CREDENTIALS
# Get these from https://my.telegram.org/apps
# =============================================================================
API_ID = "your_api_id_here"
API_HASH = "your_api_hash_here"
PHONE_NUMBER = "+your_phone_number"  # Example: "+1234567890"

# =============================================================================
# CHANNEL TO MONITOR (Choose ONE of the following)
# =============================================================================
# Option 1: Use Channel ID (for private channels you're a member of)
CHANNEL_ID = -1001234567890  # Replace with actual channel ID

# Option 2: Use Channel Username (for public channels or private with username)
CHANNEL_USERNAME = None  # Set to "@channelname" if using username instead

# Option 3: Use Channel invite link (for private channels)
CHANNEL_LINK = None  # Set to "https://t.me/joinchat/xxxxx" if using link instead

# =============================================================================
# WECHAT SETTINGS
# =============================================================================
# WeChat contact/group name to forward messages to
WECHAT_TARGET = "文件传输助手"  # Default: File Transfer Assistant
# Other examples:
# WECHAT_TARGET = "My Friend Name"      # Forward to a specific friend
# WECHAT_TARGET = "Group Chat Name"     # Forward to a group chat

# =============================================================================
# PROXY SETTINGS
# =============================================================================
PROXY_ENABLED = False  # Set to True if you need proxy
PROXY_TYPE = "socks5"  # Options: "socks5", "socks4", "http", "mtproto"
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 7890

# Optional: Proxy authentication (leave empty if not needed)
PROXY_USERNAME = ""
PROXY_PASSWORD = ""

# MTProxy specific (only if PROXY_TYPE = "mtproto")
MTPROXY_SECRET = ""  # Hex string from MTProxy

# =============================================================================
# CONNECTION SETTINGS
# =============================================================================
CONNECTION_TIMEOUT = 30
MAX_RETRIES = 5
RETRY_DELAY = 5

# =============================================================================
# OUTPUT SETTINGS
# =============================================================================
# Console output
SHOW_IN_CONSOLE = True

# File output
SAVE_TO_FILE = True
OUTPUT_FILENAME = "messages.txt"

# Session file name
SESSION_NAME = "telegram_session"

# =============================================================================
# AUTO-GENERATED CONFIG (Don't modify below this line)
# =============================================================================
def get_config():
    """Get configuration as a dictionary."""
    
    # Determine which channel method to use (priority: ID > USERNAME > LINK)
    channel_target = None
    if CHANNEL_ID:
        channel_target = CHANNEL_ID
    elif CHANNEL_USERNAME:
        channel_target = CHANNEL_USERNAME
    elif CHANNEL_LINK:
        channel_target = CHANNEL_LINK
    else:
        raise ValueError("You must specify either CHANNEL_ID, CHANNEL_USERNAME, or CHANNEL_LINK")
    
    # Build proxy config
    proxy_config = {
        "enabled": PROXY_ENABLED,
        "type": PROXY_TYPE,
        "host": PROXY_HOST,
        "port": PROXY_PORT,
        "username": PROXY_USERNAME,
        "password": PROXY_PASSWORD
    }
    
    if PROXY_TYPE == "mtproto" and MTPROXY_SECRET:
        proxy_config["secret"] = MTPROXY_SECRET
    
    return {
        "api_id": API_ID,
        "api_hash": API_HASH,
        "phone_number": PHONE_NUMBER,
        "channel_target": channel_target,
        "wechat_target": WECHAT_TARGET,
        "connection": {
            "timeout": CONNECTION_TIMEOUT,
            "max_retries": MAX_RETRIES,
            "base_delay": RETRY_DELAY
        },
        "proxy": proxy_config,
        "session_name": SESSION_NAME,
        "output": {
            "console": SHOW_IN_CONSOLE,
            "file": SAVE_TO_FILE,
            "filename": OUTPUT_FILENAME
        }
    }

# Validate configuration when imported
if __name__ == "__main__":
    try:
        config = get_config()
        print("✅ Configuration is valid!")
        print(f"📱 Phone: {config['phone_number']}")
        print(f"📺 Channel: {config['channel_target']}")
        print(f"💬 WeChat Target: {config['wechat_target']}")
        print(f"🌐 Proxy: {'Enabled' if config['proxy']['enabled'] else 'Disabled'}")
    except Exception as e:
        print(f"❌ Configuration error: {e}")