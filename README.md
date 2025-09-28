# Telegram to WeChat Forwarder# Telegram Channel Monitor



A Python application that forwards messages from Telegram channels to WeChat in real-time.A Python script to monitor Telegram channels in real-time using user account authentication and optional proxy support.



## Features## Features



- ✅ Real-time message forwarding from Telegram channels to WeChat- Real-time monitoring of Telegram channels

- ✅ Support for user account authentication (no bot token required)- User account authentication (no bot token required)

- ✅ Proxy support (HTTP, SOCKS4, SOCKS5, MTProxy)- Proxy support (HTTP and SOCKS5)

- ✅ Automatic session management- Configuration file for easy setup

- ✅ Message formatting with sender info and timestamps- Message logging to console and/or file

- ✅ Console and file logging- Automatic session management

- ✅ Error handling and reconnection

## Quick Start (Windows)

## Requirements

1. **Run the installer**: Double-click `install.bat` - this will set up the environment and dependencies

- Python 3.7+2. **Configure**: The installer will run the setup script to collect your credentials

- WeChat PC application (must be running and logged in)3. **Start monitoring**: Double-click `run_monitor.bat` or run manually

- Telegram account

- Optional: Proxy server (if needed for Telegram access)## Manual Setup



## Installation### 1. Install Dependencies



1. **Install Python dependencies:**```bash

   ```bashpip install -r requirements.txt

   pip install -r requirements.txt```

   ```

### 2. Get Telegram API Credentials

2. **Configure the application:**

   Edit `config.py` and fill in your credentials:1. Go to https://my.telegram.org/apps

   - Telegram API credentials (api_id, api_hash, phone_number)2. Log in with your Telegram account

   - Channel to monitor (channel_id, username, or invite link)3. Create a new application

   - WeChat target (contact or group name)4. Note down your `api_id` and `api_hash`

   - Proxy settings (if needed)

### 3. Configure the Script

3. **Make sure WeChat is running:**

   - Launch WeChat PC application**Option A: Interactive Setup**

   - Log in to your account```bash

   - Ensure the target contact/group existspython setup.py

```

## Configuration

**Option B: Manual Configuration**

Edit `config.py` to configure the forwarder:Edit `config.json` with your details:



### Telegram Settings```json

```python{

API_ID = "your_api_id"    "api_id": "YOUR_API_ID",

API_HASH = "your_api_hash"    "api_hash": "YOUR_API_HASH", 

PHONE_NUMBER = "+1234567890"    "phone_number": "YOUR_PHONE_NUMBER",

    "channel_username": "@channel_username",

# Channel to monitor (choose one):    "proxy": {

CHANNEL_ID = -1001234567890           # For channel ID        "enabled": false,

CHANNEL_USERNAME = "@channelname"     # For public channels        "type": "http",

CHANNEL_LINK = "https://t.me/..."     # For invite links        "host": "127.0.0.1",

```        "port": 8080,

        "username": "",

### WeChat Settings        "password": ""

```python    },

WECHAT_TARGET = "文件传输助手"  # File Transfer Assistant (default)    "session_name": "telegram_session",

# Or specify a contact/group name:    "output": {

# WECHAT_TARGET = "Friend Name"        "console": true,

# WECHAT_TARGET = "Group Chat Name"        "file": true,

```        "filename": "messages.txt"

    }

### Proxy Settings (Optional)}

```python```

PROXY_ENABLED = True

PROXY_TYPE = "socks5"        # Options: socks5, socks4, http, mtproto**Configuration Options:**

PROXY_HOST = "127.0.0.1"

PROXY_PORT = 7890- `api_id`, `api_hash`: Your Telegram API credentials

PROXY_USERNAME = ""          # Optional- `phone_number`: Your phone number (including country code, e.g., "+1234567890")

PROXY_PASSWORD = ""          # Optional- `channel_username`: Target channel username (with @ symbol)

```- `proxy.enabled`: Set to `true` to use proxy

- `proxy.type`: "http" or "socks5"

## Usage- `proxy.host`, `proxy.port`: Proxy server details

- `proxy.username`, `proxy.password`: Proxy authentication (if required)

Run the forwarder:- `session_name`: Name for the session file (will be created automatically)

```bash- `output.console`: Display messages in console

python telegram_to_wechat.py- `output.file`: Save messages to file

```- `output.filename`: Output file name



The application will:## Usage

1. Connect to Telegram (may prompt for verification code on first run)

2. Connect to WeChat### Quick Start (Windows)

3. Start forwarding messages in real-time```bash

4. Display forwarded messages in consolerun_monitor.bat

5. Log all activities to `telegram_wechat.log````



Press `Ctrl+C` to stop the forwarder.### Manual Run

```bash

## Authenticationpython telegram_monitor.py

```

### First Run (Telegram)

On the first run, you'll need to authenticate with Telegram:### Using the Example Script

1. The app will send a verification code to your phone```bash

2. Enter the 5-digit code when promptedpython example.py

3. If you have 2FA enabled, enter your password```

4. Session will be saved for future use

### First Run Authentication

### WeChatOn first run, you'll be prompted to:

- WeChat PC application must be running and logged in1. Enter the verification code sent to your Telegram account

- The target contact/group must exist in your WeChat2. Enter your 2FA password (if enabled)

- The app will send a test message to verify connection

The script will then start monitoring the specified channel and display new messages in real-time.

## Message Format

## Example Output

Forwarded messages include:

- `[Telegram]` prefix```

- Sender information (username or name)2024-01-15 14:30:25 - INFO - Successfully connected to Telegram!

- Timestamp2024-01-15 14:30:26 - INFO - Monitoring channel: Example Channel (@example_channel)

- Original message content2024-01-15 14:30:26 - INFO - Started monitoring for new messages. Press Ctrl+C to stop.

- Media indicators for files/images

[2024-01-15 14:31:45] @example_channel | @username: Hello, this is a test message!

Example:[2024-01-15 14:32:10] @example_channel | John Doe: Another message from the channel

``````

[Telegram] @username

2024-09-28 15:30:45## Notes



Hello, this is a test message!- The session file will be created after successful authentication and reused in subsequent runs

```- Messages are displayed with timestamp, channel, sender, and content

- Media messages are shown as "[Media/Sticker/Other]"

## Logging- Press Ctrl+C to stop monitoring



The application creates two types of logs:## Security

- **Console output**: Real-time message display

- **File log**: Detailed logging in `telegram_wechat.log`- Keep your `api_id`, `api_hash`, and session files secure

- Don't share your configuration file

## Troubleshooting- The session file contains authentication data - treat it like a password



### Common Issues## Troubleshooting



1. **WeChat connection failed:**1. **Import errors**: Make sure all dependencies are installed with `pip install -r requirements.txt`

   - Ensure WeChat PC app is running and logged in2. **Authentication failed**: Double-check your API credentials and phone number format

   - Check that the target contact/group name is correct3. **Channel not found**: Ensure the channel username is correct and you have access to it

   - Try using "文件传输助手" (File Transfer Assistant) as target4. **Proxy issues**: Verify proxy settings and credentials

2. **Telegram connection failed:**
   - Verify API credentials in `config.py`
   - Check proxy settings if using one
   - Ensure phone number format is correct (+country_code)

3. **Proxy issues:**
   - Test proxy connection independently
   - Verify proxy type, host, and port
   - Check username/password if required

4. **Channel not found:**
   - Ensure you're a member of the channel
   - Use correct channel ID, username, or invite link
   - For private channels, use channel ID or invite link

### Error Messages

- `❌ config.py not found`: Create and configure `config.py`
- `❌ wxauto not installed`: Run `pip install wxauto`
- `❌ Failed to connect to WeChat`: Check WeChat app status
- `❌ Failed to connect to Telegram`: Check credentials and proxy

## File Structure

```
telegram_monitor/
├── telegram_to_wechat.py    # Main application
├── config.py                # Configuration file
├── requirements.txt         # Python dependencies
├── telegram_session.session # Telegram session (auto-generated)
├── telegram_wechat.log      # Application log
└── .venv/                   # Python virtual environment
```

## Dependencies

- **telethon**: Telegram client library
- **wxauto**: WeChat automation library
- **PySocks**: Proxy support
- **requests**: HTTP requests

## Security Notes

- Keep your API credentials secure
- Don't share session files
- Use proxy if Telegram is blocked in your region
- Be aware of Telegram's rate limits

## License

This project is for educational and personal use only. Respect Telegram's and WeChat's terms of service.