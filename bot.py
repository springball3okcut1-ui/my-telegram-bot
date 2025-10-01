import json
import time
from config import BOT_TOKEN, CURRENCIES, CRYPTOS
from telegram import TelegramBot
from api import CurrencyAPI
from language import get_text

class BotCommands:
    def __init__(self):
        self.bot = TelegramBot(BOT_TOKEN)
        self.api = CurrencyAPI()
        self.user_languages = {}  # Store user language preferences
        
    def handle_update(self, update):
        """Handle incoming Telegram updates"""
        try:
            if 'message' in update:
                self.handle_message(update['message'])
            elif 'callback_query' in update:
                self.handle_callback_query(update['callback_query'])
        except Exception as e:
            print(f"Error handling update: {e}")
    
    def handle_message(self, message):
        """Handle incoming messages"""
        chat_id = message['chat']['id']
        user_id = message['from']['id']
        text = message.get('text', '')
        
        # Get user language (default to Turkish)
        user_lang = self.user_languages.get(user_id, 'tr')
        
        if text == '/start':
            self.send_start_menu(chat_id, user_lang)
        elif text == '/help':
            self.send_help(chat_id, user_lang)
        elif text == '/language':
            self.send_language_menu(chat_id, user_lang)
        else:
            # Unknown command
            welcome_text = get_text('welcome', user_lang)
            self.bot.send_message(chat_id, welcome_text, reply_markup=self.get_main_menu_keyboard(user_lang))
    
    def handle_callback_query(self, callback_query):
        """Handle callback queries from inline keyboards"""
        query_id = callback_query['id']
        chat_id = callback_query['message']['chat']['id']
        user_id = callback_query['from']['id']
        data = callback_query['data']
        
        # Get user language
        user_lang = self.user_languages.get(user_id, 'tr')
        
        # Answer callback query
        self.bot.answer_callback_query(query_id)
        
        if data.startswith('lang_'):
            # Language selection
            lang = data.split('_')[1]
            self.user_languages[user_id] = lang
            
            success_text = get_text('language_changed', lang)
            self.bot.send_message(chat_id, success_text, reply_markup=self.get_main_menu_keyboard(lang))
            
        elif data == 'currencies':
            self.send_currencies_menu(chat_id, user_lang)
            
        elif data == 'cryptos':
            self.send_cryptos_menu(chat_id, user_lang)
            
        elif data == 'converter':
            self.send_converter_menu(chat_id, user_lang)
            
        elif data == 'language':
            self.send_language_menu(chat_id, user_lang)
            
        elif data == 'back_main':
            self.send_start_menu(chat_id, user_lang)
            
        elif data.startswith('show_'):
            # Show specific currency rates
            currency = data.split('_')[1]
            self.show_currency_rates(chat_id, currency, user_lang)
            
        elif data.startswith('crypto_'):
            # Show specific crypto price
            crypto = data.split('_')[1]
            self.show_crypto_price(chat_id, crypto, user_lang)
            
        elif data.startswith('convert_'):
            # Convert currency
            parts = data.split('_')
            if len(parts) == 4:  # convert_from_to_amount
                from_curr = parts[1]
                to_curr = parts[2]
                amount = float(parts[3])
                self.convert_currency(chat_id, from_curr, to_curr, amount, user_lang)
    
    def send_start_menu(self, chat_id, user_lang='tr'):
        """Send the main menu"""
        welcome_text = get_text('welcome', user_lang)
        keyboard = self.get_main_menu_keyboard(user_lang)
        self.bot.send_message(chat_id, welcome_text, reply_markup=keyboard)
    
    def send_help(self, chat_id, user_lang='tr'):
        """Send help message"""
        help_text = get_text('help', user_lang)
        keyboard = self.get_back_keyboard(user_lang)
        self.bot.send_message(chat_id, help_text, reply_markup=keyboard)
    
    def send_language_menu(self, chat_id, user_lang='tr'):
        """Send language selection menu"""
        text = get_text('select_language', user_lang)
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": "🇹🇷 Türkçe", "callback_data": "lang_tr"},
                    {"text": "🇺🇸 English", "callback_data": "lang_en"}
                ],
                [
                    {"text": "🇷🇺 Русский", "callback_data": "lang_ru"}
                ],
                [
                    {"text": get_text('back', user_lang), "callback_data": "back_main"}
                ]
            ]
        }
        self.bot.send_message(chat_id, text, reply_markup=json.dumps(keyboard))
    
    def send_currencies_menu(self, chat_id, user_lang='tr'):
        """Send currencies menu"""
        text = get_text('select_currency', user_lang)
        keyboard_rows = []
        
        # Add currency buttons in pairs
        curr_list = list(CURRENCIES.items())
        for i in range(0, len(curr_list), 2):
            row = []
            for j in range(2):
                if i + j < len(curr_list):
                    code, info = curr_list[i + j]
                    row.append({
                        "text": f"{info['flag']} {info['name']}",
                        "callback_data": f"show_{code}"
                    })
            keyboard_rows.append(row)
        
        # Add back button
        keyboard_rows.append([{
            "text": get_text('back', user_lang),
            "callback_data": "back_main"
        }])
        
        keyboard = {"inline_keyboard": keyboard_rows}
        self.bot.send_message(chat_id, text, reply_markup=json.dumps(keyboard))
    
    def send_cryptos_menu(self, chat_id, user_lang='tr'):
        """Send cryptos menu"""
        text = get_text('select_crypto', user_lang)
        keyboard_rows = []
        
        # Add crypto buttons in pairs
        crypto_list = list(CRYPTOS.items())
        for i in range(0, len(crypto_list), 2):
            row = []
            for j in range(2):
                if i + j < len(crypto_list):
                    code, info = crypto_list[i + j]
                    row.append({
                        "text": f"{info['symbol']} {info['name']}",
                        "callback_data": f"crypto_{code}"
                    })
            keyboard_rows.append(row)
        
        # Add back button
        keyboard_rows.append([{
            "text": get_text('back', user_lang),
            "callback_data": "back_main"
        }])
        
        keyboard = {"inline_keyboard": keyboard_rows}
        self.bot.send_message(chat_id, text, reply_markup=json.dumps(keyboard))
    
    def send_converter_menu(self, chat_id, user_lang='tr'):
        """Send converter menu with quick conversion options"""
        text = get_text('converter_help', user_lang)
        keyboard_rows = []
        
        # Popular conversion pairs
        popular_pairs = [
            ('USD', 'TRY', '100'),
            ('EUR', 'TRY', '100'),
            ('TRY', 'USD', '1000'),
            ('TRY', 'EUR', '1000'),
            ('USD', 'EUR', '100'),
            ('EUR', 'USD', '100')
        ]
        
        for from_curr, to_curr, amount in popular_pairs:
            from_info = CURRENCIES.get(from_curr, {'flag': '', 'name': from_curr})
            to_info = CURRENCIES.get(to_curr, {'flag': '', 'name': to_curr})
            
            button_text = f"{amount} {from_info['flag']}{from_curr} → {to_info['flag']}{to_curr}"
            callback_data = f"convert_{from_curr}_{to_curr}_{amount}"
            
            keyboard_rows.append([{
                "text": button_text,
                "callback_data": callback_data
            }])
        
        # Add back button
        keyboard_rows.append([{
            "text": get_text('back', user_lang),
            "callback_data": "back_main"
        }])
        
        keyboard = {"inline_keyboard": keyboard_rows}
        self.bot.send_message(chat_id, text, reply_markup=json.dumps(keyboard))
    
    def show_currency_rates(self, chat_id, currency_code, user_lang='tr'):
        """Show exchange rates for a specific currency"""
        try:
            rates = self.api.get_exchange_rates(currency_code)
            
            if not rates:
                error_text = get_text('api_error', user_lang)
                self.bot.send_message(chat_id, error_text)
                return
            
            currency_info = CURRENCIES.get(currency_code, {'flag': '', 'name': currency_code})
            
            # Build message
            message_lines = [
                f"{currency_info['flag']} {currency_info['name']} ({currency_code})",
                f"📅 {get_text('last_update', user_lang)}: {time.strftime('%Y-%m-%d %H:%M')}",
                ""
            ]
            
            # Show rates for all other currencies
            for target_code, target_info in CURRENCIES.items():
                if target_code != currency_code and target_code in rates:
                    rate = rates[target_code]
                    message_lines.append(
                        f"{target_info['flag']} 1 {currency_code} = {rate:.4f} {target_code}"
                    )
            
            message_text = "\n".join(message_lines)
            keyboard = self.get_back_keyboard(user_lang, 'currencies')
            
            self.bot.send_message(chat_id, message_text, reply_markup=keyboard)
            
        except Exception as e:
            error_text = get_text('api_error', user_lang)
            self.bot.send_message(chat_id, f"{error_text}\n\nError: {str(e)}")
    
    def show_crypto_price(self, chat_id, crypto_code, user_lang='tr'):
        """Show cryptocurrency price"""
        try:
            prices = self.api.get_crypto_prices([crypto_code])
            
            if not prices or crypto_code not in prices:
                error_text = get_text('api_error', user_lang)
                self.bot.send_message(chat_id, error_text)
                return
            
            crypto_info = CRYPTOS.get(crypto_code, {'symbol': '', 'name': crypto_code})
            price_data = prices[crypto_code]
            
            # Build message
            message_lines = [
                f"{crypto_info['symbol']} {crypto_info['name']} ({crypto_code.upper()})",
                f"📅 {get_text('last_update', user_lang)}: {time.strftime('%Y-%m-%d %H:%M')}",
                ""
            ]
            
            # Show prices in different currencies
            for currency in ['usd', 'eur', 'try']:
                if currency in price_data:
                    curr_info = CURRENCIES.get(currency.upper(), {'flag': '', 'symbol': currency.upper()})
                    price = price_data[currency]
                    message_lines.append(
                        f"{curr_info['flag']} {price:.2f} {currency.upper()}"
                    )
            
            # Show 24h change if available
            if 'usd_24h_change' in price_data:
                change = price_data['usd_24h_change']
                change_emoji = "📈" if change >= 0 else "📉"
                message_lines.append(f"\n{change_emoji} 24h: {change:+.2f}%")
            
            message_text = "\n".join(message_lines)
            keyboard = self.get_back_keyboard(user_lang, 'cryptos')
            
            self.bot.send_message(chat_id, message_text, reply_markup=keyboard)
            
        except Exception as e:
            error_text = get_text('api_error', user_lang)
            self.bot.send_message(chat_id, f"{error_text}\n\nError: {str(e)}")
    
    def convert_currency(self, chat_id, from_curr, to_curr, amount, user_lang='tr'):
        """Convert currency amount"""
        try:
            result = self.api.convert_currency(from_curr, to_curr, amount)
            
            if result is None:
                error_text = get_text('api_error', user_lang)
                self.bot.send_message(chat_id, error_text)
                return
            
            from_info = CURRENCIES.get(from_curr, {'flag': '', 'name': from_curr})
            to_info = CURRENCIES.get(to_curr, {'flag': '', 'name': to_curr})
            
            message_text = f"""💱 {get_text('conversion_result', user_lang)}

{from_info['flag']} {amount:,.2f} {from_curr}
⬇️
{to_info['flag']} {result:,.2f} {to_curr}

📅 {get_text('last_update', user_lang)}: {time.strftime('%Y-%m-%d %H:%M')}"""
            
            keyboard = self.get_back_keyboard(user_lang, 'converter')
            self.bot.send_message(chat_id, message_text, reply_markup=keyboard)
            
        except Exception as e:
            error_text = get_text('api_error', user_lang)
            self.bot.send_message(chat_id, f"{error_text}\n\nError: {str(e)}")
    
    def get_main_menu_keyboard(self, user_lang='tr'):
        """Get main menu inline keyboard"""
        keyboard = {
            "inline_keyboard": [
                [
                    {"text": f"💰 {get_text('currencies', user_lang)}", "callback_data": "currencies"},
                    {"text": f"₿ {get_text('cryptos', user_lang)}", "callback_data": "cryptos"}
                ],
                [
                    {"text": f"💱 {get_text('converter', user_lang)}", "callback_data": "converter"}
                ],
                [
                    {"text": f"🌐 {get_text('language', user_lang)}", "callback_data": "language"}
                ]
            ]
        }
        return json.dumps(keyboard)
    
    def get_back_keyboard(self, user_lang='tr', back_to='back_main'):
        """Get back button keyboard"""
        keyboard = {
            "inline_keyboard": [
                [{"text": get_text('back', user_lang), "callback_data": back_to}]
            ]
        }
        return json.dumps(keyboard)