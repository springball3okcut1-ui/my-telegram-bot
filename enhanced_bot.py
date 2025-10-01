#!/usr/bin/env python3
"""
Enhanced Currency Bot using python-telegram-bot library
This version provides better error handling, logging, and features
"""

import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from config import BOT_TOKEN, CURRENCIES, CRYPTOS
from api import CurrencyAPI
from language import get_text

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class EnhancedCurrencyBot:
    def __init__(self):
        self.api = CurrencyAPI()
        self.user_languages = {}  # Store user language preferences
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a message when the command /start is issued."""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        user_lang = self.user_languages.get(user_id, 'tr')
        
        welcome_text = get_text('welcome', user_lang)
        keyboard = self.get_main_menu_keyboard(user_lang)
        
        await update.message.reply_text(welcome_text, reply_markup=keyboard)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send help message."""
        user_id = update.effective_user.id
        user_lang = self.user_languages.get(user_id, 'tr')
        
        help_text = get_text('help', user_lang)
        keyboard = self.get_back_keyboard(user_lang)
        
        await update.message.reply_text(help_text, reply_markup=keyboard)
    
    async def language_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send language selection menu."""
        user_id = update.effective_user.id
        user_lang = self.user_languages.get(user_id, 'tr')
        
        await self.send_language_menu(update, user_lang)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle button callbacks."""
        query = update.callback_query
        user_id = query.from_user.id
        user_lang = self.user_languages.get(user_id, 'tr')
        data = query.data
        
        await query.answer()
        
        if data.startswith('lang_'):
            # Language selection
            lang = data.split('_')[1]
            self.user_languages[user_id] = lang
            
            success_text = get_text('language_changed', lang)
            keyboard = self.get_main_menu_keyboard(lang)
            
            await query.edit_message_text(success_text, reply_markup=keyboard)
            
        elif data == 'currencies':
            await self.send_currencies_menu(query, user_lang)
            
        elif data == 'cryptos':
            await self.send_cryptos_menu(query, user_lang)
            
        elif data == 'converter':
            await self.send_converter_menu(query, user_lang)
            
        elif data == 'language':
            await self.send_language_menu(query, user_lang)
            
        elif data == 'back_main':
            await self.send_main_menu(query, user_lang)
            
        elif data.startswith('show_'):
            # Show specific currency rates
            currency = data.split('_')[1]
            await self.show_currency_rates(query, currency, user_lang)
            
        elif data.startswith('crypto_'):
            # Show specific crypto price
            crypto = data.split('_')[1]
            await self.show_crypto_price(query, crypto, user_lang)
            
        elif data.startswith('convert_'):
            # Convert currency
            parts = data.split('_')
            if len(parts) == 4:
                from_curr = parts[1]
                to_curr = parts[2]
                amount = float(parts[3])
                await self.convert_currency(query, from_curr, to_curr, amount, user_lang)
    
    async def send_main_menu(self, query_or_update, user_lang='tr'):
        """Send main menu."""
        welcome_text = get_text('welcome', user_lang)
        keyboard = self.get_main_menu_keyboard(user_lang)
        
        if hasattr(query_or_update, 'edit_message_text'):
            await query_or_update.edit_message_text(welcome_text, reply_markup=keyboard)
        else:
            await query_or_update.message.reply_text(welcome_text, reply_markup=keyboard)
    
    async def send_language_menu(self, query_or_update, user_lang='tr'):
        """Send language selection menu."""
        text = get_text('select_language', user_lang)
        
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇹🇷 Türkçe", callback_data="lang_tr"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ],
            [
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")
            ],
            [
                InlineKeyboardButton(get_text('back', user_lang), callback_data="back_main")
            ]
        ])
        
        if hasattr(query_or_update, 'edit_message_text'):
            await query_or_update.edit_message_text(text, reply_markup=keyboard)
        else:
            await query_or_update.message.reply_text(text, reply_markup=keyboard)
    
    async def send_currencies_menu(self, query, user_lang='tr'):
        """Send currencies menu."""
        text = get_text('select_currency', user_lang)
        buttons = []
        
        # Add currency buttons in pairs
        curr_list = list(CURRENCIES.items())
        for i in range(0, len(curr_list), 2):
            row = []
            for j in range(2):
                if i + j < len(curr_list):
                    code, info = curr_list[i + j]
                    row.append(InlineKeyboardButton(
                        f"{info['flag']} {info['name']}",
                        callback_data=f"show_{code}"
                    ))
            buttons.append(row)
        
        # Add back button
        buttons.append([InlineKeyboardButton(
            get_text('back', user_lang),
            callback_data="back_main"
        )])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text, reply_markup=keyboard)
    
    async def send_cryptos_menu(self, query, user_lang='tr'):
        """Send cryptos menu."""
        text = get_text('select_crypto', user_lang)
        buttons = []
        
        # Add crypto buttons in pairs
        crypto_list = list(CRYPTOS.items())
        for i in range(0, len(crypto_list), 2):
            row = []
            for j in range(2):
                if i + j < len(crypto_list):
                    code, info = crypto_list[i + j]
                    row.append(InlineKeyboardButton(
                        f"{info['symbol']} {info['name']}",
                        callback_data=f"crypto_{code}"
                    ))
            buttons.append(row)
        
        # Add back button
        buttons.append([InlineKeyboardButton(
            get_text('back', user_lang),
            callback_data="back_main"
        )])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text, reply_markup=keyboard)
    
    async def send_converter_menu(self, query, user_lang='tr'):
        """Send converter menu."""
        text = get_text('converter_help', user_lang)
        buttons = []
        
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
            
            buttons.append([InlineKeyboardButton(
                button_text,
                callback_data=f"convert_{from_curr}_{to_curr}_{amount}"
            )])
        
        # Add back button
        buttons.append([InlineKeyboardButton(
            get_text('back', user_lang),
            callback_data="back_main"
        )])
        
        keyboard = InlineKeyboardMarkup(buttons)
        await query.edit_message_text(text, reply_markup=keyboard)
    
    async def show_currency_rates(self, query, currency_code, user_lang='tr'):
        """Show exchange rates for a specific currency."""
        try:
            rates = self.api.get_exchange_rates(currency_code)
            
            if not rates:
                error_text = get_text('api_error', user_lang)
                await query.edit_message_text(error_text)
                return
            
            currency_info = CURRENCIES.get(currency_code, {'flag': '', 'name': currency_code})
            
            message_lines = [
                f"{currency_info['flag']} {currency_info['name']} ({currency_code})",
                f"📅 {get_text('last_update', user_lang)}: {self.get_current_time()}",
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
            
            await query.edit_message_text(message_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error showing currency rates: {e}")
            error_text = get_text('api_error', user_lang)
            await query.edit_message_text(f"{error_text}\n\nError: {str(e)}")
    
    async def show_crypto_price(self, query, crypto_code, user_lang='tr'):
        """Show cryptocurrency price."""
        try:
            prices = self.api.get_crypto_prices([crypto_code])
            
            if not prices or crypto_code not in prices:
                error_text = get_text('api_error', user_lang)
                await query.edit_message_text(error_text)
                return
            
            crypto_info = CRYPTOS.get(crypto_code, {'symbol': '', 'name': crypto_code})
            price_data = prices[crypto_code]
            
            message_lines = [
                f"{crypto_info['symbol']} {crypto_info['name']} ({crypto_code.upper()})",
                f"📅 {get_text('last_update', user_lang)}: {self.get_current_time()}",
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
            
            await query.edit_message_text(message_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error showing crypto price: {e}")
            error_text = get_text('api_error', user_lang)
            await query.edit_message_text(f"{error_text}\n\nError: {str(e)}")
    
    async def convert_currency(self, query, from_curr, to_curr, amount, user_lang='tr'):
        """Convert currency amount."""
        try:
            result = self.api.convert_currency(from_curr, to_curr, amount)
            
            if result is None:
                error_text = get_text('api_error', user_lang)
                await query.edit_message_text(error_text)
                return
            
            from_info = CURRENCIES.get(from_curr, {'flag': '', 'name': from_curr})
            to_info = CURRENCIES.get(to_curr, {'flag': '', 'name': to_curr})
            
            message_text = f"""💱 {get_text('conversion_result', user_lang)}

{from_info['flag']} {amount:,.2f} {from_curr}
⬇️
{to_info['flag']} {result:,.2f} {to_curr}

📅 {get_text('last_update', user_lang)}: {self.get_current_time()}"""
            
            keyboard = self.get_back_keyboard(user_lang, 'converter')
            await query.edit_message_text(message_text, reply_markup=keyboard)
            
        except Exception as e:
            logger.error(f"Error converting currency: {e}")
            error_text = get_text('api_error', user_lang)
            await query.edit_message_text(f"{error_text}\n\nError: {str(e)}")
    
    def get_main_menu_keyboard(self, user_lang='tr'):
        """Get main menu inline keyboard."""
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(f"💰 {get_text('currencies', user_lang)}", callback_data="currencies"),
                InlineKeyboardButton(f"₿ {get_text('cryptos', user_lang)}", callback_data="cryptos")
            ],
            [
                InlineKeyboardButton(f"💱 {get_text('converter', user_lang)}", callback_data="converter")
            ],
            [
                InlineKeyboardButton(f"🌐 {get_text('language', user_lang)}", callback_data="language")
            ]
        ])
    
    def get_back_keyboard(self, user_lang='tr', back_to='back_main'):
        """Get back button keyboard."""
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(get_text('back', user_lang), callback_data=back_to)]
        ])
    
    def get_current_time(self):
        """Get current time formatted."""
        import time
        return time.strftime('%Y-%m-%d %H:%M')

def main():
    """Start the bot."""
    print("🚀 Enhanced Currency Bot Starting...")
    print("Using python-telegram-bot library")
    print("=" * 50)
    
    # Create the Application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Create bot instance
    bot = EnhancedCurrencyBot()
    
    # Register handlers
    application.add_handler(CommandHandler("start", bot.start))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(CommandHandler("language", bot.language_command))
    application.add_handler(CallbackQueryHandler(bot.button_callback))
    
    # Start the bot
    print("✅ Bot handlers registered")
    print("🔄 Starting polling...")
    print("📱 Send /start to your bot to test")
    print("-" * 50)
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()