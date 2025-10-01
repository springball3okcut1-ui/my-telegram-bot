#!/usr/bin/env python3
"""
Telegram Currency Bot - Polling Mode
Run this file locally to test the bot using long polling.
"""

import time
from bot import BotCommands

def main():
    """Main polling loop"""
    print("🤖 Currency Bot - Polling Mode")
    print("="*50)
    
    # Initialize bot commands handler
    bot_handler = BotCommands()
    
    # Get initial offset
    offset = 0
    
    print("✅ Bot started successfully!")
    print("💡 Press Ctrl+C to stop the bot")
    print("📱 Send /start to your bot to begin")
    print("-"*50)
    
    try:
        while True:
            try:
                # Get updates from Telegram
                updates = bot_handler.bot.get_updates(offset=offset, timeout=30)
                
                if updates:
                    for update in updates:
                        try:
                            # Handle each update
                            bot_handler.handle_update(update)
                            
                            # Update offset to avoid processing same update twice
                            offset = update['update_id'] + 1
                            
                            # Log the update
                            if 'message' in update:
                                user = update['message']['from']
                                text = update['message'].get('text', '[non-text]')
                                print(f"📨 Message from {user.get('first_name', 'Unknown')} (@{user.get('username', 'no_username')}): {text}")
                            elif 'callback_query' in update:
                                user = update['callback_query']['from']
                                data = update['callback_query']['data']
                                print(f"🔘 Callback from {user.get('first_name', 'Unknown')} (@{user.get('username', 'no_username')}): {data}")
                                
                        except Exception as e:
                            print(f"❌ Error handling update {update.get('update_id', 'unknown')}: {e}")
                            continue
                else:
                    # No updates, just wait a bit
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\n🛑 Bot stopped by user")
                break
            except Exception as e:
                print(f"❌ Polling error: {e}")
                print("⏳ Retrying in 5 seconds...")
                time.sleep(5)
                continue
    
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    
    print("👋 Bot shutdown complete")

if __name__ == "__main__":
    main()