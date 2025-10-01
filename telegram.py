import requests
import json
import time
from config import BOT_TOKEN

class TelegramBot:
    """Telegram Bot API wrapper"""
    
    def __init__(self, token):
        self.token = token
        self.api_url = f"https://api.telegram.org/bot{token}/"
        self.session = requests.Session()
    
    def send_message(self, chat_id, text, reply_markup=None):
        """Send message to user"""
        data = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        return self._make_request('sendMessage', data)
    
    def edit_message_text(self, chat_id, message_id, text, reply_markup=None):
        """Edit message text"""
        data = {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        
        if reply_markup:
            data['reply_markup'] = json.dumps(reply_markup)
        
        return self._make_request('editMessageText', data)
    
    def answer_callback_query(self, callback_query_id, text=None, show_alert=False):
        """Answer callback query"""
        data = {'callback_query_id': callback_query_id}
        
        if text:
            data['text'] = text
        if show_alert:
            data['show_alert'] = True
        
        return self._make_request('answerCallbackQuery', data)
    
    def get_updates(self, offset=0, timeout=30):
        """Get updates (for polling mode)"""
        try:
            params = {
                'offset': offset,
                'timeout': timeout
            }
            
            response = self.session.get(
                self.api_url + 'getUpdates',
                params=params,
                timeout=timeout + 5
            )
            response.raise_for_status()
            
            data = response.json()
            return data.get('result', [])
        except Exception as e:
            print(f"Error getting updates: {e}")
            return []
    
    def set_webhook(self, url):
        """Set webhook URL"""
        return self._make_request('setWebhook', {'url': url})
    
    def delete_webhook(self):
        """Delete webhook"""
        return self._make_request('deleteWebhook', {})
    
    def get_me(self):
        """Get bot information"""
        return self._make_request('getMe', {})
    
    def get_webhook_info(self):
        """Get webhook information"""
        return self._make_request('getWebhookInfo', {})
    
    def _make_request(self, method, data):
        """Make API request to Telegram"""
        try:
            response = self.session.post(
                self.api_url + method,
                data=data,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Telegram API error ({method}): {e}")
            return {'ok': False, 'description': str(e)}
    
    def create_inline_keyboard(self, buttons):
        """Create inline keyboard markup"""
        return {'inline_keyboard': buttons}
    
    def create_keyboard(self, buttons, resize=True, one_time=False):
        """Create regular keyboard markup"""
        return {
            'keyboard': buttons,
            'resize_keyboard': resize,
            'one_time_keyboard': one_time
        }