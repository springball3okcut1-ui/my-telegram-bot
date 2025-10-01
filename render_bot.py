#!/usr/bin/env python3
"""
Render.com Deployment Runner
This file is specifically designed to run the Currency Bot on Render.com
Supports both original and enhanced bot implementations
"""

import os
import sys
import time

def main():
    """Main function for Render deployment"""
    print("🚀 Currency Bot starting on Render...")
    print("=" * 50)
    
    # Check if running on Render
    if os.environ.get('RENDER'):
        print("✅ Running on Render.com")
        print(f"📍 Service: {os.environ.get('RENDER_SERVICE_NAME', 'Unknown')}")
    else:
        print("ℹ️ Running in development mode")
    
    # Check for bot token
    bot_token = os.environ.get('BOT_TOKEN')
    if bot_token:
        print("✅ Bot token loaded from environment")
    else:
        print("ℹ️ Using bot token from config.py")
    
    # Try enhanced bot first, fallback to original
    try:
        print("🔍 Checking for python-telegram-bot library...")
        import telegram
        print("✅ python-telegram-bot found - using enhanced bot")
        from enhanced_bot import main as enhanced_main
        enhanced_main()
        
    except ImportError:
        print("ℹ️ python-telegram-bot not available - creating fallback bot")
        try:
            # Create a simple fallback bot using basic imports
            print("🔄 Starting fallback polling bot...")
            import json
            import time
            import urllib.request
            import urllib.parse
            from config import BOT_TOKEN, CURRENCIES, CRYPTOS
            from language import get_text
            
            # Simple Telegram API
            TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"
            
            def send_request(method, params=None):
                try:
                    url = f"{TELEGRAM_API}/{method}"
                    if params:
                        data = urllib.parse.urlencode(params).encode('utf-8')
                        request = urllib.request.Request(url, data=data)
                    else:
                        request = urllib.request.Request(url)
                    
                    with urllib.request.urlopen(request, timeout=10) as response:
                        return json.loads(response.read().decode('utf-8'))
                except Exception as e:
                    print(f"API Error: {e}")
                    return None
            
            def get_updates(offset=0):
                params = {'offset': offset, 'timeout': 30}
                return send_request('getUpdates', params)
            
            def send_message(chat_id, text):
                params = {'chat_id': chat_id, 'text': text}
                return send_request('sendMessage', params)
            
            def handle_message(message):
                chat_id = message['chat']['id']
                text = message.get('text', '').lower().strip()
                
                if text == '/start':
                    welcome = get_text('welcome', 'tr')
                    send_message(chat_id, welcome)
                elif text == '/help':
                    help_text = get_text('help', 'tr')
                    send_message(chat_id, help_text)
                else:
                    welcome = get_text('welcome', 'tr')
                    send_message(chat_id, welcome)
            
            print("✅ Fallback bot initialized")
            print("🔄 Starting polling mode...")
            print("📱 Bot is ready to receive messages")
            print("-" * 50)
            
            offset = 0
            while True:
                try:
                    response = get_updates(offset)
                    if response and response.get('ok'):
                        updates = response.get('result', [])
                        for update in updates:
                            offset = update['update_id'] + 1
                            if 'message' in update:
                                handle_message(update['message'])
                                user = update['message']['from']
                                text = update['message'].get('text', '[non-text]')
                                print(f"📨 {user.get('first_name', 'User')}: {text}")
                    time.sleep(1)
                except KeyboardInterrupt:
                    print("\n🛑 Bot stopped")
                    break
                except Exception as e:
                    print(f"❌ Polling error: {e}")
                    time.sleep(5)
                    continue
                    
        except Exception as e:
            print(f"❌ Failed to start fallback bot: {e}")
            sys.exit(1)
                
    except Exception as e:
        print(f"❌ Failed to start enhanced bot: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
