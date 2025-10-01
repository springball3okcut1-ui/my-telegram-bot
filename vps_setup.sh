#!/bin/bash

# Currency Bot VPS Quick Setup Script
# Bu script VPS'te botunuzu hızlıca kurmak için kullanılır

set -e  # Hata durumunda scripti durdur

echo "🚀 Currency Bot VPS Kurulumu Başlatılıyor..."

# Renkli çıktı için
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Fonksiyonlar
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Root kontrolü
if [ "$EUID" -ne 0 ]; then
    print_error "Bu script root olarak çalıştırılmalıdır!"
    exit 1
fi

# Sistem güncellemesi
print_status "Sistem güncelleniyor..."
apt update && apt upgrade -y

# Gerekli paketleri kur
print_status "Gerekli paketler kuruluyor..."
apt install -y python3 python3-pip python3-venv curl wget git htop

# Proje dizini oluştur
print_status "Proje dizini oluşturuluyor..."
mkdir -p /opt/currency_bot
cd /opt/currency_bot

# Virtual environment oluştur
print_status "Python virtual environment oluşturuluyor..."
python3 -m venv venv
source venv/bin/activate

# Gerekli Python paketlerini kur
print_status "Python paketleri kuruluyor..."
pip install --upgrade pip
pip install python-telegram-bot==20.7 requests

# Bot dosyalarını oluştur
print_status "Bot dosyaları oluşturuluyor..."

# currency_bot.py dosyasını oluştur
cat > currency_bot.py << 'EOF'
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

def main():
    """Main function to run the bot"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_amount))
    
    # Start the bot
    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
EOF

# Systemd service dosyasını oluştur
print_status "Systemd service oluşturuluyor..."
cat > /etc/systemd/system/currency-bot.service << 'EOF'
[Unit]
Description=Currency Exchange Telegram Bot
After=network.target
Wants=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/opt/currency_bot
Environment=PATH=/opt/currency_bot/venv/bin
Environment=PYTHONPATH=/opt/currency_bot
ExecStart=/opt/currency_bot/venv/bin/python /opt/currency_bot/currency_bot.py
ExecReload=/bin/kill -HUP $MAINPID
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=currency-bot

# Güvenlik ayarları
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/opt/currency_bot

[Install]
WantedBy=multi-user.target
EOF

# Service'i etkinleştir ve başlat
print_status "Service başlatılıyor..."
systemctl daemon-reload
systemctl enable currency-bot
systemctl start currency-bot

# Durumu kontrol et
sleep 3
if systemctl is-active --quiet currency-bot; then
    print_status "✅ Bot başarıyla başlatıldı!"
else
    print_error "❌ Bot başlatılamadı!"
    print_status "Logları kontrol edin: journalctl -u currency-bot -f"
    exit 1
fi

# Başarı mesajı
echo ""
echo "🎉 Currency Bot VPS kurulumu tamamlandı!"
echo ""
echo "📊 Bot durumu:"
systemctl status currency-bot --no-pager -l
echo ""
echo "📋 Yararlı komutlar:"
echo "  • Bot logları: journalctl -u currency-bot -f"
echo "  • Bot durumu: systemctl status currency-bot"
echo "  • Botu durdur: systemctl stop currency-bot"
echo "  • Botu başlat: systemctl start currency-bot"
echo "  • Botu yeniden başlat: systemctl restart currency-bot"
echo ""
echo "🔗 Telegram'da botunuzu test edin!"
echo "   Bot Token: 7968532349:AAFGFSe_aFShl7NMa9S1R_tjkC9IyoUGMTI"
echo ""
print_status "Kurulum tamamlandı! Bot şu anda çalışıyor."





