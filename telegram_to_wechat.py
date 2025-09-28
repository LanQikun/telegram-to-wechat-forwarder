#!/usr/bin/env python3
"""
Telegram to WeChat Forwarder
Forwards all messages from a Telegram channel to WeChat's "文件传输助手"
"""

import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
import sys
import socks

try:
    from wxauto import WeChat
except ImportError:
    print("❌ wxauto not installed. Please run: pip install wxauto")
    sys.exit(1)

# Import our config
try:
    import config
except ImportError:
    print("❌ config.py not found. Please create it first.")
    sys.exit(1)

class TelegramToWeChatForwarder:
    def __init__(self):
        """Initialize the forwarder with configuration."""
        self.config = config.get_config()
        self.client = None
        self.wechat = None
        self.setup_logging()
        
    def setup_logging(self):
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('telegram_wechat.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def setup_wechat(self):
        """Initialize WeChat connection."""
        try:
            self.logger.info("🟢 Connecting to WeChat...")
            self.wechat = WeChat()
            
            # Test connection to WeChat target directly
            wechat_target = self.config['wechat_target']
            try:
                # Try to switch to the target chat
                self.wechat.ChatWith(wechat_target)
                self.logger.info(f"✅ Successfully connected to '{wechat_target}'")
                
                # Send a test message to verify connection
                test_msg = "🤖 Telegram forwarder connection test"
                self.wechat.SendMsg(test_msg)
                self.logger.info("✅ Test message sent successfully")
                
                return True
                
            except Exception as e:
                self.logger.error(f"❌ Failed to connect to '{wechat_target}': {e}")
                
                # Try to get available chats
                try:
                    # Get current chat list (method varies by wxauto version)
                    current_chats = []
                    try:
                        # Try newer method first
                        current_chats = self.wechat.GetAllMessage()
                    except:
                        try:
                            # Try alternative method
                            current_chats = self.wechat.GetSessionList()
                        except:
                            pass
                    
                    if current_chats:
                        self.logger.info("Available chats:")
                        for chat in current_chats[:5]:  # Show first 5
                            self.logger.info(f"  - {chat}")
                    
                except Exception as list_error:
                    self.logger.warning(f"Could not get chat list: {list_error}")
                
                self.logger.info(f"💡 Make sure '{wechat_target}' exists in your WeChat contacts")
                return False
                
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize WeChat: {e}")
            self.logger.info("💡 Make sure WeChat PC app is running and logged in")
            return False
    
    def setup_proxy(self):
        """Setup proxy configuration if enabled."""
        proxy_config = self.config.get('proxy', {})
        
        if not proxy_config.get('enabled', False):
            return None
        
        proxy_type = proxy_config.get('type', 'http').lower()
        host = proxy_config.get('host', '127.0.0.1')
        port = proxy_config.get('port', 8080)
        username = proxy_config.get('username', '')
        password = proxy_config.get('password', '')
        
        try:
            if proxy_type == 'mtproto':
                # MTProxy configuration
                secret = proxy_config.get('secret', '')
                if not secret:
                    self.logger.error("MTProxy secret is required")
                    return None
                
                try:
                    secret_bytes = bytes.fromhex(secret)
                except ValueError:
                    self.logger.error("Invalid MTProxy secret format")
                    return None
                
                self.logger.info(f"Using MTProxy: {host}:{port}")
                return (proxy_type, host, port, secret_bytes)
            
            elif proxy_type == 'http':
                import socks
                proxy = (socks.HTTP, host, port)
                if username and password:
                    proxy = (socks.HTTP, host, port, True, username, password)
            elif proxy_type == 'socks5':
                import socks
                proxy = (socks.SOCKS5, host, port)
                if username and password:
                    proxy = (socks.SOCKS5, host, port, True, username, password)
            elif proxy_type == 'socks4':
                import socks
                proxy = (socks.SOCKS4, host, port)
                if username and password:
                    proxy = (socks.SOCKS4, host, port, True, username, password)
            else:
                self.logger.warning(f"Unsupported proxy type: {proxy_type}")
                return None
            
            self.logger.info(f"Using {proxy_type.upper()} proxy: {host}:{port}")
            return proxy
            
        except ImportError:
            self.logger.error("PySocks not available. Install it with: pip install PySocks")
            return None
    
    async def initialize_telegram_client(self):
        """Initialize and connect the Telegram client."""
        try:
            proxy = self.setup_proxy()
            
            self.client = TelegramClient(
                self.config['session_name'],
                self.config['api_id'],
                self.config['api_hash'],
                proxy=proxy,
                timeout=self.config.get('connection', {}).get('timeout', 30)
            )
            
            self.logger.info("🔵 Connecting to Telegram...")
            await self.client.start(phone=self.config['phone_number'])
            
            if not await self.client.is_user_authorized():
                self.logger.info(f"Requesting verification code for {self.config['phone_number']}")
                await self.client.send_code_request(self.config['phone_number'])
                
                try:
                    print(f"\n🔐 AUTHENTICATION REQUIRED")
                    print(f"📱 Check your phone {self.config['phone_number']} for a verification code")
                    code = input('\n📋 Enter the 5-digit code: ')
                    
                    await self.client.sign_in(self.config['phone_number'], code.strip())
                    self.logger.info("✅ Successfully authenticated!")
                    
                except SessionPasswordNeededError:
                    print(f"\n🔒 Two-Factor Authentication (2FA) is enabled")
                    password = input('🔑 Enter your 2FA password: ')
                    await self.client.sign_in(password=password)
                    self.logger.info("✅ Successfully authenticated with 2FA!")
            
            self.logger.info("✅ Connected to Telegram!")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to connect to Telegram: {e}")
            return False
    
    def send_to_wechat(self, message_text):
        """Send message to WeChat target."""
        try:
            wechat_target = self.config['wechat_target']
            
            # Make sure we're in the right chat
            self.wechat.ChatWith(wechat_target)
            
            # Send the message
            self.wechat.SendMsg(message_text)
            
            self.logger.info(f"✅ Sent to '{wechat_target}': {message_text[:50]}{'...' if len(message_text) > 50 else ''}")
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Failed to send to WeChat: {e}")
            return False
    
    def format_message(self, event):
        """Format Telegram message for WeChat."""
        message = event.message
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Get sender info
        sender_info = "Unknown"
        if message.sender:
            if hasattr(message.sender, 'username') and message.sender.username:
                sender_info = f"@{message.sender.username}"
            elif hasattr(message.sender, 'first_name'):
                sender_info = message.sender.first_name
                if hasattr(message.sender, 'last_name') and message.sender.last_name:
                    sender_info += f" {message.sender.last_name}"
        
        # Get message content
        if message.text:
            content = message.text
        elif message.media:
            content = "[📷 Media/File]"
        else:
            content = "[📄 Other content]"
        
        # Format the message for WeChat
        formatted = f"[Telegram] {sender_info}\n{timestamp}\n\n{content}"
        return formatted
    
    async def start_forwarding(self):
        """Start forwarding messages from Telegram to WeChat."""
        # Initialize WeChat first
        if not self.setup_wechat():
            self.logger.error("❌ Cannot continue without WeChat connection")
            return
        
        # Initialize Telegram
        if not await self.initialize_telegram_client():
            self.logger.error("❌ Cannot continue without Telegram connection")
            return
        
        try:
            # Get the channel entity
            channel_target = self.config['channel_target']
            self.logger.info(f"🎯 Getting channel: {channel_target}")
            
            channel = await self.client.get_entity(channel_target)
            self.logger.info(f"✅ Found channel: {channel.title} (ID: {channel.id})")
            
            # Setup message handler
            @self.client.on(events.NewMessage(chats=channel))
            async def handle_new_message(event):
                try:
                    formatted_message = self.format_message(event)
                    
                    # Send to WeChat
                    success = self.send_to_wechat(formatted_message)
                    
                    if success:
                        # Also log to console if enabled
                        if self.config.get('output', {}).get('console', True):
                            print(f"\n📨 Forwarded: {formatted_message}")
                        
                        # Save to file if enabled
                        if self.config.get('output', {}).get('file', False):
                            filename = self.config.get('output', {}).get('filename', 'forwarded_messages.txt')
                            try:
                                with open(filename, 'a', encoding='utf-8') as f:
                                    f.write(formatted_message + '\n\n')
                            except Exception as e:
                                self.logger.error(f"Failed to save to file: {e}")
                    
                except Exception as e:
                    self.logger.error(f"❌ Error handling message: {e}")
            
            wechat_target = self.config['wechat_target']
            
            self.logger.info("🚀 Started forwarding Telegram → WeChat")
            self.logger.info("Press Ctrl+C to stop...")
            print(f"\n🔄 Forwarding messages from '{channel.title}' to WeChat '{wechat_target}'")
            print("📱 New messages will appear here and in WeChat")
            print("⏹️  Press Ctrl+C to stop\n")
            
            # Keep running
            await self.client.run_until_disconnected()
            
        except Exception as e:
            self.logger.error(f"❌ Error during forwarding: {e}")
        finally:
            if self.client:
                await self.client.disconnect()
                self.logger.info("🔴 Disconnected from Telegram")

async def main():
    """Main function to run the forwarder."""
    print("🔄 Telegram → WeChat Forwarder")
    print("=" * 35)
    
    forwarder = TelegramToWeChatForwarder()
    
    try:
        await forwarder.start_forwarding()
    except KeyboardInterrupt:
        print("\n👋 Forwarding stopped by user.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("\n🔧 Make sure:")
        print("1. WeChat is running and logged in")
        print("2. Your proxy (if enabled) is running") 
        print("3. Your Telegram credentials are correct")

if __name__ == "__main__":
    asyncio.run(main())