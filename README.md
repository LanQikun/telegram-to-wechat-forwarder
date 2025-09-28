# Telegram to WeChat Forwarder

Real-time message forwarding from Telegram channels to WeChat.

## Features
- ✅ Real-time forwarding with user authentication (no bot needed)
- ✅ Proxy support (HTTP/SOCKS4/SOCKS5/MTProxy)  
- ✅ Message formatting with timestamps and sender info
- ✅ Automatic session management and logging

## Quick Start

### Windows (Recommended)
1. **Run installer:** Double-click `install.bat`
2. **Configure:** Edit `config.py` with your credentials
3. **Start:** Run `python telegram_to_wechat.py`

### Manual Setup
```bash
pip install -r requirements.txt
cp config_template.py config.py  # Edit with your details
python telegram_to_wechat.py
```

## Configuration

Get your Telegram API credentials from https://my.telegram.org/apps

Edit `config.py`:
```python
API_ID = "your_api_id"
API_HASH = "your_api_hash"  
PHONE_NUMBER = "+1234567890"
CHANNEL_ID = -1001234567890  # Channel to monitor
WECHAT_TARGET = "文件传输助手"  # WeChat target
PROXY_ENABLED = False
PROXY_TYPE = "socks5"
PROXY_HOST = "127.0.0.1"
PROXY_PORT = 7890
```

## Requirements
- Python 3.7+
- WeChat PC app (running and logged in)
- **WeChat version below 4.1 is required** (newer versions may not work with wxauto)
- Telegram account

## Authentication
First run will prompt for:
1. SMS verification code
2. 2FA password (if enabled)

Session is saved automatically.

## Message Format
```
[Telegram] @username
2024-09-28 15:30:45

Hello, this is a test message!
```

## Troubleshooting

**WeChat connection failed:**
- Ensure WeChat PC app is running and logged in
- **Use WeChat version below 4.1** (newer versions incompatible with wxauto)
- Check target contact/group name exists

**Telegram connection failed:**
- Verify API credentials
- Check proxy settings if using one
- Ensure correct phone number format

**Channel not found:**
- Confirm you're a member of the channel
- Use correct channel ID/username/invite link

## Files
- `telegram_to_wechat.py` - Main application
- `config.py` - Your configuration (created from template)
- `config_template.py` - Configuration template
- `requirements.txt` - Dependencies
- `install.bat` - Windows installer

## Security
- Never share your `config.py` or session files
- Keep API credentials secure
- Use proxy if Telegram is blocked

## License
For educational and personal use. Respect Telegram and WeChat terms of service.
