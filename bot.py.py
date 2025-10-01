import logging
import requests
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import asyncio
from datetime import datetime

# Bot token
BOT_TOKEN = "7968532349:AAFGFSe_aFShl7NMa9S1R_tjkC9IyoUGMTI"

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Currency codes mapping
CURRENCY_CODES = {
    'TRY': 'Turkish Lira',
    'AZN': 'Azerbaijani Manat', 
    'RUB': 'Russian Ruble',
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'BNB': 'Binance Coin',
    'ADA': 'Cardano',
    'SOL': 'Solana',
    'XRP': 'Ripple',
    'DOT': 'Polkadot',
    'DOGE': 'Dogecoin',
    'MATIC': 'Polygon',
    'AVAX': 'Avalanche',
    'LINK': 'Chainlink',
    'UNI': 'Uniswap',
    'LTC': 'Litecoin',
    'ATOM': 'Cosmos',
    'FTM': 'Fantom',
    'ALGO': 'Algorand',
    'VET': 'VeChain',
    'FIL': 'Filecoin',
    'TRX': 'TRON',
    'XLM': 'Stellar',
    'MANA': 'Decentraland',
    'SAND': 'The Sandbox',
    'AXS': 'Axie Infinity',
    'CHZ': 'Chiliz',
    'ENJ': 'Enjin Coin',
    'BAT': 'Basic Attention Token',
    'ZEC': 'Zcash',
    'DASH': 'Dash',
    'NEO': 'NEO',
    'QTUM': 'Qtum',
    'ICX': 'ICON',
    'ONT': 'Ontology',
    'ZIL': 'Zilliqa',
    'WAVES': 'Waves',
    'KSM': 'Kusama',
    'GRT': 'The Graph',
    'COMP': 'Compound',
    'YFI': 'Yearn.finance',
    'SNX': 'Synthetix',
    'MKR': 'Maker',
    'AAVE': 'Aave',
    'CRV': 'Curve DAO Token',
    '1INCH': '1inch',
    'SUSHI': 'SushiSwap',
    'CAKE': 'PancakeSwap',
    'SHIB': 'Shiba Inu',
    'PEPE': 'Pepe',
    'FLOKI': 'Floki',
    'BONK': 'Bonk'
}

# Language support
LANGUAGES = {
    'tr': {
        'welcome': 'Hoş geldiniz! Para birimi botuna hoş geldiniz.',
        'main_menu': 'Ana Menü',
        'current_rates': 'Güncel Kurlar',
        'currency_comparison': 'Para Birimi Karşılaştırması',
        'crypto_rates': 'Kripto Para Kurları',
        'language_select': 'Dil Seçin',
        'enter_amount': 'Karşılaştırma için miktar girin:',
        'select_currency': 'Para birimi seçin:',
        'from_currency': 'Hangi para biriminden:',
        'to_currency': 'Hangi para birimine:',
        'error': 'Hata oluştu. Lütfen tekrar deneyin.',
        'invalid_amount': 'Geçersiz miktar. Lütfen sayı girin.',
        'rate_not_found': 'Kur bulunamadı.',
        'back': 'Geri',
        'result': 'Sonuç:',
        'quick_tip': 'İpucu: Direkt olarak \'20 USD AZN\' şeklinde yazabilirsiniz!'
    },
    'en': {
        'welcome': 'Welcome! Welcome to the currency bot.',
        'main_menu': 'Main Menu',
        'current_rates': 'Current Rates',
        'currency_comparison': 'Currency Comparison',
        'crypto_rates': 'Cryptocurrency Rates',
        'language_select': 'Select Language',
        'enter_amount': 'Enter amount for comparison:',
        'select_currency': 'Select currency:',
        'from_currency': 'From currency:',
        'to_currency': 'To currency:',
        'error': 'An error occurred. Please try again.',
        'invalid_amount': 'Invalid amount. Please enter a number.',
        'rate_not_found': 'Exchange rate not found.',
        'back': 'Back',
        'result': 'Result:',
        'quick_tip': 'Tip: You can type directly like \'20 USD AZN\'!'
    },
    'ru': {
        'welcome': 'Добро пожаловать! Добро пожаловать в валютный бот.',
        'main_menu': 'Главное меню',
        'current_rates': 'Текущие курсы',
        'currency_comparison': 'Сравнение валют',
        'crypto_rates': 'Курсы криптовалют',
        'language_select': 'Выберите язык',
        'enter_amount': 'Введите сумму для сравнения:',
        'select_currency': 'Выберите валюту:',
        'from_currency': 'Из валюты:',
        'to_currency': 'В валюту:',
        'error': 'Произошла ошибка. Пожалуйста, попробуйте снова.',
        'invalid_amount': 'Неверная сумма. Пожалуйста, введите число.',
        'rate_not_found': 'Курс не найден.',
        'back': 'Назад',
        'result': 'Результат:',
        'quick_tip': 'Совет: Можете писать напрямую как \'20 USD AZN\'!'
    }
}

# User language preferences
user_languages = {}

def get_user_language(user_id):
    return user_languages.get(user_id, 'tr')

def get_text(user_id, key):
    lang = get_user_language(user_id)
    return LANGUAGES[lang].get(key, LANGUAGES['tr'][key])

async def get_exchange_rates():
    """Get current exchange rates from API"""
    try:
        # Using exchangerate-api.com for free rates
        response = requests.get('https://api.exchangerate-api.com/v4/latest/USD')
        if response.status_code == 200:
            return response.json()['rates']
        else:
            # Fallback to fixer.io if available
            response = requests.get('https://api.fixer.io/latest?base=USD')
            if response.status_code == 200:
                return response.json()['rates']
    except Exception as e:
        logger.error(f"Error fetching exchange rates: {e}")
    return None

async def get_crypto_rates():
    """Get current cryptocurrency rates"""
    try:
        # Extended list of cryptocurrencies
        crypto_ids = [
            'bitcoin', 'ethereum', 'binancecoin', 'cardano', 'solana',
            'ripple', 'polkadot', 'dogecoin', 'polygon', 'avalanche-2',
            'chainlink', 'uniswap', 'litecoin', 'cosmos', 'fantom',
            'algorand', 'vechain', 'filecoin', 'tron', 'stellar',
            'decentraland', 'the-sandbox', 'axie-infinity', 'chiliz',
            'enjincoin', 'basic-attention-token', 'zcash', 'dash',
            'neo', 'qtum', 'icon', 'ontology', 'zilliqa', 'waves',
            'kusama', 'the-graph', 'compound-governance-token',
            'yearn-finance', 'havven', 'maker', 'aave', 'curve-dao-token',
            '1inch', 'sushiswap', 'pancakeswap-token', 'shiba-inu',
            'pepe', 'floki', 'bonk'
        ]
        
        ids_string = ','.join(crypto_ids)
        response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={ids_string}&vs_currencies=usd')
        
        if response.status_code == 200:
            data = response.json()
            crypto_rates = {}
            crypto_mapping = {
                'bitcoin': 'BTC', 'ethereum': 'ETH', 'binancecoin': 'BNB',
                'cardano': 'ADA', 'solana': 'SOL', 'ripple': 'XRP',
                'polkadot': 'DOT', 'dogecoin': 'DOGE', 'polygon': 'MATIC',
                'avalanche-2': 'AVAX', 'chainlink': 'LINK', 'uniswap': 'UNI',
                'litecoin': 'LTC', 'cosmos': 'ATOM', 'fantom': 'FTM',
                'algorand': 'ALGO', 'vechain': 'VET', 'filecoin': 'FIL',
                'tron': 'TRX', 'stellar': 'XLM', 'decentraland': 'MANA',
                'the-sandbox': 'SAND', 'axie-infinity': 'AXS', 'chiliz': 'CHZ',
                'enjincoin': 'ENJ', 'basic-attention-token': 'BAT',
                'zcash': 'ZEC', 'dash': 'DASH', 'neo': 'NEO', 'qtum': 'QTUM',
                'icon': 'ICX', 'ontology': 'ONT', 'zilliqa': 'ZIL',
                'waves': 'WAVES', 'kusama': 'KSM', 'the-graph': 'GRT',
                'compound-governance-token': 'COMP', 'yearn-finance': 'YFI',
                'havven': 'SNX', 'maker': 'MKR', 'aave': 'AAVE',
                'curve-dao-token': 'CRV', '1inch': '1INCH', 'sushiswap': 'SUSHI',
                'pancakeswap-token': 'CAKE', 'shiba-inu': 'SHIB',
                'pepe': 'PEPE', 'floki': 'FLOKI', 'bonk': 'BONK'
            }
            
            for coin_id, symbol in crypto_mapping.items():
                if coin_id in data:
                    crypto_rates[symbol] = data[coin_id]['usd']
            return crypto_rates
    except Exception as e:
        logger.error(f"Error fetching crypto rates: {e}")
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command handler"""
    user_id = update.effective_user.id
    
    # Only set default language if user hasn't selected one before
    if user_id not in user_languages:
        user_languages[user_id] = 'tr'  # Default to Turkish
    
    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'current_rates'), callback_data='current_rates')],
        [InlineKeyboardButton(get_text(user_id, 'currency_comparison'), callback_data='currency_comparison')],
        [InlineKeyboardButton(get_text(user_id, 'crypto_rates'), callback_data='crypto_rates')],
        [InlineKeyboardButton(get_text(user_id, 'language_select'), callback_data='language_select')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Get user's language
    lang = get_user_language(user_id)
    
    welcome_text = f"{get_text(user_id, 'welcome')}\n\n"
    
    if lang == 'tr':
        welcome_text += "💡 **Hızlı Kullanım:**\n"
        welcome_text += "• `20 USD AZN` - 20 dolar kaç manat?\n"
        welcome_text += "• `100 BTC TRY` - 100 bitcoin kaç lira?\n"
        welcome_text += "• `50 ETH EUR` - 50 ethereum kaç euro?\n"
        welcome_text += "• `1000 TRY USD` - 1000 lira kaç dolar?\n\n"
        welcome_text += "Direkt mesaj olarak yazabilirsiniz!"
    elif lang == 'en':
        welcome_text += "💡 **Quick Usage:**\n"
        welcome_text += "• `20 USD AZN` - How much is 20 dollars in manat?\n"
        welcome_text += "• `100 BTC TRY` - How much is 100 bitcoin in lira?\n"
        welcome_text += "• `50 ETH EUR` - How much is 50 ethereum in euro?\n"
        welcome_text += "• `1000 TRY USD` - How much is 1000 lira in dollars?\n\n"
        welcome_text += "You can type directly as a message!"
    elif lang == 'ru':
        welcome_text += "💡 **Быстрое использование:**\n"
        welcome_text += "• `20 USD AZN` - Сколько манат в 20 долларах?\n"
        welcome_text += "• `100 BTC TRY` - Сколько лир в 100 биткоинах?\n"
        welcome_text += "• `50 ETH EUR` - Сколько евро в 50 эфириумах?\n"
        welcome_text += "• `1000 TRY USD` - Сколько долларов в 1000 лирах?\n\n"
        welcome_text += "Можете писать напрямую как сообщение!"
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command handler"""
    user_id = update.effective_user.id
    lang = get_user_language(user_id)
    
    if lang == 'tr':
        help_text = "🤖 **Para Birimi Botu Yardım**\n\n"
        help_text += "**Hızlı Dönüşüm:**\n"
        help_text += "• `20 USD AZN` - 20 dolar kaç manat?\n"
        help_text += "• `100 BTC TRY` - 100 bitcoin kaç lira?\n"
        help_text += "• `50 ETH EUR` - 50 ethereum kaç euro?\n"
        help_text += "• `1000 TRY USD` - 1000 lira kaç dolar?\n\n"
        help_text += "**Desteklenen Para Birimleri:**\n"
        help_text += "🇹🇷 TRY 🇦🇿 AZN 🇷🇺 RUB 🇺🇸 USD 🇪🇺 EUR 🇬🇧 GBP\n"
        help_text += "₿ BTC Ξ ETH 🟡 BNB 🔵 ADA 🟣 SOL 💧 XRP\n"
        help_text += "🔴 DOT 🐕 DOGE 🟣 MATIC 🔺 AVAX\n\n"
        help_text += "**Komutlar:**\n"
        help_text += "• `/start` - Ana menü\n"
        help_text += "• `/help` - Bu yardım mesajı\n\n"
        help_text += "**Özellikler:**\n"
        help_text += "• Güncel döviz kurları\n"
        help_text += "• Kripto para fiyatları\n"
        help_text += "• Para birimi dönüşümü\n"
        help_text += "• 3 dil desteği (TR/EN/RU)"
    elif lang == 'en':
        help_text = "🤖 **Currency Bot Help**\n\n"
        help_text += "**Quick Conversion:**\n"
        help_text += "• `20 USD AZN` - How much is 20 dollars in manat?\n"
        help_text += "• `100 BTC TRY` - How much is 100 bitcoin in lira?\n"
        help_text += "• `50 ETH EUR` - How much is 50 ethereum in euro?\n"
        help_text += "• `1000 TRY USD` - How much is 1000 lira in dollars?\n\n"
        help_text += "**Supported Currencies:**\n"
        help_text += "🇹🇷 TRY 🇦🇿 AZN 🇷🇺 RUB 🇺🇸 USD 🇪🇺 EUR 🇬🇧 GBP\n"
        help_text += "₿ BTC Ξ ETH 🟡 BNB 🔵 ADA 🟣 SOL 💧 XRP\n"
        help_text += "🔴 DOT 🐕 DOGE 🟣 MATIC 🔺 AVAX\n\n"
        help_text += "**Commands:**\n"
        help_text += "• `/start` - Main menu\n"
        help_text += "• `/help` - This help message\n\n"
        help_text += "**Features:**\n"
        help_text += "• Current exchange rates\n"
        help_text += "• Cryptocurrency prices\n"
        help_text += "• Currency conversion\n"
        help_text += "• 3 language support (TR/EN/RU)"
    elif lang == 'ru':
        help_text = "🤖 **Помощь валютного бота**\n\n"
        help_text += "**Быстрое конвертирование:**\n"
        help_text += "• `20 USD AZN` - Сколько манат в 20 долларах?\n"
        help_text += "• `100 BTC TRY` - Сколько лир в 100 биткоинах?\n"
        help_text += "• `50 ETH EUR` - Сколько евро в 50 эфириумах?\n"
        help_text += "• `1000 TRY USD` - Сколько долларов в 1000 лирах?\n\n"
        help_text += "**Поддерживаемые валюты:**\n"
        help_text += "🇹🇷 TRY 🇦🇿 AZN 🇷🇺 RUB 🇺🇸 USD 🇪🇺 EUR 🇬🇧 GBP\n"
        help_text += "₿ BTC Ξ ETH 🟡 BNB 🔵 ADA 🟣 SOL 💧 XRP\n"
        help_text += "🔴 DOT 🐕 DOGE 🟣 MATIC 🔺 AVAX\n\n"
        help_text += "**Команды:**\n"
        help_text += "• `/start` - Главное меню\n"
        help_text += "• `/help` - Это сообщение помощи\n\n"
        help_text += "**Возможности:**\n"
        help_text += "• Текущие курсы валют\n"
        help_text += "• Цены криптовалют\n"
        help_text += "• Конвертация валют\n"
        help_text += "• Поддержка 3 языков (TR/EN/RU)"
    
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    if query.data == 'current_rates':
        await show_current_rates(query, context)
    elif query.data == 'currency_comparison':
        await show_currency_comparison_menu(query, context)
    elif query.data == 'crypto_rates':
        await show_crypto_rates(query, context)
    elif query.data == 'language_select':
        await show_language_menu(query, context)
    elif query.data.startswith('lang_'):
        lang = query.data.split('_')[1]
        user_languages[user_id] = lang
        await show_main_menu(query, context)
    elif query.data.startswith('from_'):
        currency = query.data.split('_')[1]
        context.user_data['from_currency'] = currency
        await show_to_currency_menu(query, context)
    elif query.data.startswith('to_'):
        currency = query.data.split('_')[1]
        context.user_data['to_currency'] = currency
        await ask_amount(query, context)
    elif query.data == 'back_to_main':
        await show_main_menu(query, context)

async def show_current_rates(query, context):
    """Show current exchange rates"""
    user_id = query.from_user.id
    rates = await get_exchange_rates()
    
    if not rates:
        await query.edit_message_text(get_text(user_id, 'error'))
        return
    
    text = f"📊 {get_text(user_id, 'current_rates')}\n\n"
    text += f"🇹🇷 TRY: 1 USD = {rates.get('TRY', 'N/A'):.2f} TRY\n"
    text += f"🇦🇿 AZN: 1 USD = {rates.get('AZN', 'N/A'):.2f} AZN\n"
    text += f"🇷🇺 RUB: 1 USD = {rates.get('RUB', 'N/A'):.2f} RUB\n"
    text += f"🇺🇸 USD: 1 USD = 1.00 USD\n"
    text += f"🇪🇺 EUR: 1 USD = {rates.get('EUR', 'N/A'):.2f} EUR\n"
    text += f"🇬🇧 GBP: 1 USD = {rates.get('GBP', 'N/A'):.2f} GBP\n"
    
    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_crypto_rates(query, context):
    """Show cryptocurrency rates"""
    user_id = query.from_user.id
    crypto_rates = await get_crypto_rates()
    
    if not crypto_rates:
        await query.edit_message_text(get_text(user_id, 'error'))
        return
    
    text = f"₿ {get_text(user_id, 'crypto_rates')}\n\n"
    
    # Top cryptocurrencies
    top_crypto = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'MATIC', 'AVAX']
    crypto_emojis = {
        'BTC': '₿', 'ETH': 'Ξ', 'BNB': '🟡', 'ADA': '🔵', 'SOL': '🟣',
        'XRP': '💧', 'DOT': '🔴', 'DOGE': '🐕', 'MATIC': '🟣', 'AVAX': '🔺'
    }
    
    for symbol in top_crypto:
        if symbol in crypto_rates:
            emoji = crypto_emojis.get(symbol, '💰')
            price = crypto_rates[symbol]
            if price >= 1:
                text += f"{emoji} {symbol}: ${price:,.2f}\n"
            else:
                text += f"{emoji} {symbol}: ${price:.6f}\n"
    
    text += "\n📈 Diğer Popüler Kripto Paralar:\n"
    
    # Other popular cryptocurrencies
    other_crypto = ['LINK', 'UNI', 'LTC', 'ATOM', 'FTM', 'ALGO', 'VET', 'FIL', 'TRX', 'XLM']
    for symbol in other_crypto:
        if symbol in crypto_rates:
            price = crypto_rates[symbol]
            if price >= 1:
                text += f"• {symbol}: ${price:,.2f}\n"
            else:
                text += f"• {symbol}: ${price:.6f}\n"
    
    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(text, reply_markup=reply_markup)

async def show_currency_comparison_menu(query, context):
    """Show currency comparison menu"""
    user_id = query.from_user.id
    
    keyboard = [
        [InlineKeyboardButton("🇹🇷 TRY", callback_data='from_TRY'),
         InlineKeyboardButton("🇦🇿 AZN", callback_data='from_AZN'),
         InlineKeyboardButton("🇷🇺 RUB", callback_data='from_RUB')],
        [InlineKeyboardButton("🇺🇸 USD", callback_data='from_USD'),
         InlineKeyboardButton("🇪🇺 EUR", callback_data='from_EUR'),
         InlineKeyboardButton("🇬🇧 GBP", callback_data='from_GBP')],
        [InlineKeyboardButton("₿ BTC", callback_data='from_BTC'),
         InlineKeyboardButton("Ξ ETH", callback_data='from_ETH'),
         InlineKeyboardButton("🟡 BNB", callback_data='from_BNB')],
        [InlineKeyboardButton("🔵 ADA", callback_data='from_ADA'),
         InlineKeyboardButton("🟣 SOL", callback_data='from_SOL'),
         InlineKeyboardButton("💧 XRP", callback_data='from_XRP')],
        [InlineKeyboardButton("🔴 DOT", callback_data='from_DOT'),
         InlineKeyboardButton("🐕 DOGE", callback_data='from_DOGE'),
         InlineKeyboardButton("🟣 MATIC", callback_data='from_MATIC')],
        [InlineKeyboardButton("🔺 AVAX", callback_data='from_AVAX'),
         InlineKeyboardButton("🔗 LINK", callback_data='from_LINK'),
         InlineKeyboardButton("🦄 UNI", callback_data='from_UNI')],
        [InlineKeyboardButton("⚡ LTC", callback_data='from_LTC'),
         InlineKeyboardButton("🌌 ATOM", callback_data='from_ATOM'),
         InlineKeyboardButton("👻 FTM", callback_data='from_FTM')],
        [InlineKeyboardButton("🔵 ALGO", callback_data='from_ALGO'),
         InlineKeyboardButton("📺 VET", callback_data='from_VET'),
         InlineKeyboardButton("📁 FIL", callback_data='from_FIL')],
        [InlineKeyboardButton("🌐 TRX", callback_data='from_TRX'),
         InlineKeyboardButton("⭐ XLM", callback_data='from_XLM'),
         InlineKeyboardButton("🎮 MANA", callback_data='from_MANA')],
        [InlineKeyboardButton("🏖️ SAND", callback_data='from_SAND'),
         InlineKeyboardButton("🎯 AXS", callback_data='from_AXS'),
         InlineKeyboardButton("⚽ CHZ", callback_data='from_CHZ')],
        [InlineKeyboardButton("💎 ENJ", callback_data='from_ENJ'),
         InlineKeyboardButton("🦇 BAT", callback_data='from_BAT'),
         InlineKeyboardButton("🔒 ZEC", callback_data='from_ZEC')],
        [InlineKeyboardButton("💨 DASH", callback_data='from_DASH'),
         InlineKeyboardButton("🔵 NEO", callback_data='from_NEO'),
         InlineKeyboardButton("🔷 QTUM", callback_data='from_QTUM')],
        [InlineKeyboardButton("🟠 ICX", callback_data='from_ICX'),
         InlineKeyboardButton("🔷 ONT", callback_data='from_ONT'),
         InlineKeyboardButton("⚡ ZIL", callback_data='from_ZIL')],
        [InlineKeyboardButton("🌊 WAVES", callback_data='from_WAVES'),
         InlineKeyboardButton("🟣 KSM", callback_data='from_KSM'),
         InlineKeyboardButton("📊 GRT", callback_data='from_GRT')],
        [InlineKeyboardButton("🏛️ COMP", callback_data='from_COMP'),
         InlineKeyboardButton("💰 YFI", callback_data='from_YFI'),
         InlineKeyboardButton("🔗 SNX", callback_data='from_SNX')],
        [InlineKeyboardButton("🏭 MKR", callback_data='from_MKR'),
         InlineKeyboardButton("🏦 AAVE", callback_data='from_AAVE'),
         InlineKeyboardButton("🔄 CRV", callback_data='from_CRV')],
        [InlineKeyboardButton("1️⃣ 1INCH", callback_data='from_1INCH'),
         InlineKeyboardButton("🍣 SUSHI", callback_data='from_SUSHI'),
         InlineKeyboardButton("🥞 CAKE", callback_data='from_CAKE')],
        [InlineKeyboardButton("🐕 SHIB", callback_data='from_SHIb'),
         InlineKeyboardButton("🐸 PEPE", callback_data='from_PEPE'),
         InlineKeyboardButton("🐕 FLOKI", callback_data='from_FLOKI')],
        [InlineKeyboardButton("🐕 BONK", callback_data='from_BONK')],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{get_text(user_id, 'from_currency')}\n\n💡 {get_text(user_id, 'quick_tip')}",
        reply_markup=reply_markup
    )

async def show_to_currency_menu(query, context):
    """Show target currency selection menu"""
    user_id = query.from_user.id
    from_currency = context.user_data.get('from_currency')
    
    keyboard = [
        [InlineKeyboardButton("🇹🇷 TRY", callback_data='to_TRY'),
         InlineKeyboardButton("🇦🇿 AZN", callback_data='to_AZN'),
         InlineKeyboardButton("🇷🇺 RUB", callback_data='to_RUB')],
        [InlineKeyboardButton("🇺🇸 USD", callback_data='to_USD'),
         InlineKeyboardButton("🇪🇺 EUR", callback_data='to_EUR'),
         InlineKeyboardButton("🇬🇧 GBP", callback_data='to_GBP')],
        [InlineKeyboardButton("₿ BTC", callback_data='to_BTC'),
         InlineKeyboardButton("Ξ ETH", callback_data='to_ETH'),
         InlineKeyboardButton("🟡 BNB", callback_data='to_BNB')],
        [InlineKeyboardButton("🔵 ADA", callback_data='to_ADA'),
         InlineKeyboardButton("🟣 SOL", callback_data='to_SOL'),
         InlineKeyboardButton("💧 XRP", callback_data='to_XRP')],
        [InlineKeyboardButton("🔴 DOT", callback_data='to_DOT'),
         InlineKeyboardButton("🐕 DOGE", callback_data='to_DOGE'),
         InlineKeyboardButton("🟣 MATIC", callback_data='to_MATIC')],
        [InlineKeyboardButton("🔺 AVAX", callback_data='to_AVAX'),
         InlineKeyboardButton("🔗 LINK", callback_data='to_LINK'),
         InlineKeyboardButton("🦄 UNI", callback_data='to_UNI')],
        [InlineKeyboardButton("⚡ LTC", callback_data='to_LTC'),
         InlineKeyboardButton("🌌 ATOM", callback_data='to_ATOM'),
         InlineKeyboardButton("👻 FTM", callback_data='to_FTM')],
        [InlineKeyboardButton("🔵 ALGO", callback_data='to_ALGO'),
         InlineKeyboardButton("📺 VET", callback_data='to_VET'),
         InlineKeyboardButton("📁 FIL", callback_data='to_FIL')],
        [InlineKeyboardButton("🌐 TRX", callback_data='to_TRX'),
         InlineKeyboardButton("⭐ XLM", callback_data='to_XLM'),
         InlineKeyboardButton("🎮 MANA", callback_data='to_MANA')],
        [InlineKeyboardButton("🏖️ SAND", callback_data='to_SAND'),
         InlineKeyboardButton("🎯 AXS", callback_data='to_AXS'),
         InlineKeyboardButton("⚽ CHZ", callback_data='to_CHZ')],
        [InlineKeyboardButton("💎 ENJ", callback_data='to_ENJ'),
         InlineKeyboardButton("🦇 BAT", callback_data='to_BAT'),
         InlineKeyboardButton("🔒 ZEC", callback_data='to_ZEC')],
        [InlineKeyboardButton("💨 DASH", callback_data='to_DASH'),
         InlineKeyboardButton("🔵 NEO", callback_data='to_NEO'),
         InlineKeyboardButton("🔷 QTUM", callback_data='to_QTUM')],
        [InlineKeyboardButton("🟠 ICX", callback_data='to_ICX'),
         InlineKeyboardButton("🔷 ONT", callback_data='to_ONT'),
         InlineKeyboardButton("⚡ ZIL", callback_data='to_ZIL')],
        [InlineKeyboardButton("🌊 WAVES", callback_data='to_WAVES'),
         InlineKeyboardButton("🟣 KSM", callback_data='to_KSM'),
         InlineKeyboardButton("📊 GRT", callback_data='to_GRT')],
        [InlineKeyboardButton("🏛️ COMP", callback_data='to_COMP'),
         InlineKeyboardButton("💰 YFI", callback_data='to_YFI'),
         InlineKeyboardButton("🔗 SNX", callback_data='to_SNX')],
        [InlineKeyboardButton("🏭 MKR", callback_data='to_MKR'),
         InlineKeyboardButton("🏦 AAVE", callback_data='to_AAVE'),
         InlineKeyboardButton("🔄 CRV", callback_data='to_CRV')],
        [InlineKeyboardButton("1️⃣ 1INCH", callback_data='to_1INCH'),
         InlineKeyboardButton("🍣 SUSHI", callback_data='to_SUSHI'),
         InlineKeyboardButton("🥞 CAKE", callback_data='to_CAKE')],
        [InlineKeyboardButton("🐕 SHIB", callback_data='to_SHIb'),
         InlineKeyboardButton("🐸 PEPE", callback_data='to_PEPE'),
         InlineKeyboardButton("🐕 FLOKI", callback_data='to_FLOKI')],
        [InlineKeyboardButton("🐕 BONK", callback_data='to_BONK')],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{get_text(user_id, 'to_currency')}\n\n💡 {get_text(user_id, 'quick_tip')}",
        reply_markup=reply_markup
    )

async def ask_amount(query, context):
    """Ask user for amount to convert"""
    user_id = query.from_user.id
    from_currency = context.user_data.get('from_currency')
    to_currency = context.user_data.get('to_currency')
    
    context.user_data['waiting_for_amount'] = True
    
    keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"{get_text(user_id, 'enter_amount')}\n\n{from_currency} → {to_currency}",
        reply_markup=reply_markup
    )

def parse_conversion_input(text):
    """Parse text input like '20 USD AZN' or '100 BTC TRY'"""
    import re
    
    # Pattern to match: number currency1 currency2
    pattern = r'(\d+(?:\.\d+)?)\s+([A-Za-z]+)\s+([A-Za-z]+)'
    match = re.match(pattern, text.strip().upper())
    
    if match:
        amount = float(match.group(1))
        from_currency = match.group(2).upper()
        to_currency = match.group(3).upper()
        
        # Validate currencies
        if from_currency in CURRENCY_CODES and to_currency in CURRENCY_CODES:
            return amount, from_currency, to_currency
    
    return None, None, None

async def handle_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle amount input for conversion"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Check if it's a direct conversion command like "20 USD AZN"
    amount, from_currency, to_currency = parse_conversion_input(text)
    
    if amount is not None:
        # Direct conversion command
        rates = await get_exchange_rates()
        crypto_rates = await get_crypto_rates()
        
        if not rates and not crypto_rates:
            await update.message.reply_text(get_text(user_id, 'error'))
            return
        
        result = await calculate_conversion(amount, from_currency, to_currency, rates, crypto_rates)
        
        if result is None:
            await update.message.reply_text(get_text(user_id, 'rate_not_found'))
            return
        
        text_result = f"{get_text(user_id, 'result')}\n\n"
        text_result += f"{amount:,.2f} {from_currency} = {result:,.2f} {to_currency}"
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text_result, reply_markup=reply_markup)
        return
    
    # Original amount input handling
    if not context.user_data.get('waiting_for_amount'):
        return
    
    try:
        amount = float(text)
        from_currency = context.user_data.get('from_currency')
        to_currency = context.user_data.get('to_currency')
        
        # Get exchange rates
        rates = await get_exchange_rates()
        crypto_rates = await get_crypto_rates()
        
        if not rates and not crypto_rates:
            await update.message.reply_text(get_text(user_id, 'error'))
            return
        
        # Calculate conversion
        result = await calculate_conversion(amount, from_currency, to_currency, rates, crypto_rates)
        
        if result is None:
            await update.message.reply_text(get_text(user_id, 'rate_not_found'))
            return
        
        text_result = f"{get_text(user_id, 'result')}\n\n"
        text_result += f"{amount:,.2f} {from_currency} = {result:,.2f} {to_currency}"
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(text_result, reply_markup=reply_markup)
        
        # Clear waiting state
        context.user_data['waiting_for_amount'] = False
        
    except ValueError:
        await update.message.reply_text(get_text(user_id, 'invalid_amount'))

async def calculate_conversion(amount, from_currency, to_currency, rates, crypto_rates):
    """Calculate currency conversion"""
    try:
        # Define all supported cryptocurrencies
        crypto_currencies = [
            'BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'XRP', 'DOT', 'DOGE', 'MATIC', 'AVAX',
            'LINK', 'UNI', 'LTC', 'ATOM', 'FTM', 'ALGO', 'VET', 'FIL', 'TRX', 'XLM',
            'MANA', 'SAND', 'AXS', 'CHZ', 'ENJ', 'BAT', 'ZEC', 'DASH', 'NEO', 'QTUM',
            'ICX', 'ONT', 'ZIL', 'WAVES', 'KSM', 'GRT', 'COMP', 'YFI', 'SNX', 'MKR',
            'AAVE', 'CRV', '1INCH', 'SUSHI', 'CAKE', 'SHIB', 'PEPE', 'FLOKI', 'BONK'
        ]
        
        # Handle crypto to crypto conversions
        if from_currency in crypto_currencies and to_currency in crypto_currencies:
            if crypto_rates and from_currency in crypto_rates and to_currency in crypto_rates:
                # Convert through USD
                from_usd = crypto_rates[from_currency]
                to_usd = crypto_rates[to_currency]
                return amount * from_usd / to_usd
        
        # Handle crypto to fiat conversions
        elif from_currency in crypto_currencies:
            if crypto_rates and from_currency in crypto_rates and rates:
                crypto_usd = crypto_rates[from_currency]
                if to_currency == 'USD':
                    return amount * crypto_usd
                elif to_currency in rates:
                    return amount * crypto_usd * rates[to_currency]
        
        # Handle fiat to crypto conversions
        elif to_currency in crypto_currencies:
            if rates and crypto_rates and to_currency in crypto_rates:
                if from_currency == 'USD':
                    return amount / crypto_rates[to_currency]
                elif from_currency in rates:
                    usd_amount = amount / rates[from_currency]
                    return usd_amount / crypto_rates[to_currency]
        
        # Handle fiat to fiat conversions
        else:
            if rates and from_currency in rates and to_currency in rates:
                if from_currency == 'USD':
                    return amount * rates[to_currency]
                elif to_currency == 'USD':
                    return amount / rates[from_currency]
                else:
                    # Convert through USD
                    usd_amount = amount / rates[from_currency]
                    return usd_amount * rates[to_currency]
        
        return None
    except Exception as e:
        logger.error(f"Error calculating conversion: {e}")
        return None

async def show_language_menu(query, context):
    """Show language selection menu"""
    user_id = query.from_user.id
    
    keyboard = [
        [InlineKeyboardButton("🇹🇷 Türkçe", callback_data='lang_tr')],
        [InlineKeyboardButton("🇺🇸 English", callback_data='lang_en')],
        [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
        [InlineKeyboardButton(get_text(user_id, 'back'), callback_data='back_to_main')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text(user_id, 'language_select'),
        reply_markup=reply_markup
    )

async def show_main_menu(query, context):
    """Show main menu"""
    user_id = query.from_user.id
    
    keyboard = [
        [InlineKeyboardButton(get_text(user_id, 'current_rates'), callback_data='current_rates')],
        [InlineKeyboardButton(get_text(user_id, 'currency_comparison'), callback_data='currency_comparison')],
        [InlineKeyboardButton(get_text(user_id, 'crypto_rates'), callback_data='crypto_rates')],
        [InlineKeyboardButton(get_text(user_id, 'language_select'), callback_data='language_select')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        get_text(user_id, 'main_menu'),
        reply_markup=reply_markup
    )

def main():
    """Main function to run the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))
    
    # Start the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
