# Currency Bot Configuration
BOT_TOKEN = "7968532349:AAFGFSe_aFShl7NMa9S1R_tjkC9IyoUGMTI"

# Supported currencies for Turkey, Azerbaijan, Russia, America, Europe
CURRENCIES = {
    'TRY': {'name': 'Turkish Lira', 'flag': '🇹🇷', 'symbol': '₺'},
    'AZN': {'name': 'Azerbaijani Manat', 'flag': '🇦🇿', 'symbol': '₼'},
    'RUB': {'name': 'Russian Ruble', 'flag': '🇷🇺', 'symbol': '₽'},
    'USD': {'name': 'US Dollar', 'flag': '🇺🇸', 'symbol': '$'},
    'EUR': {'name': 'Euro', 'flag': '🇪🇺', 'symbol': '€'},
    'GBP': {'name': 'British Pound', 'flag': '🇬🇧', 'symbol': '£'},
    'JPY': {'name': 'Japanese Yen', 'flag': '🇯🇵', 'symbol': '¥'},
    'CAD': {'name': 'Canadian Dollar', 'flag': '🇨🇦', 'symbol': 'C$'},
    'CHF': {'name': 'Swiss Franc', 'flag': '🇨🇭', 'symbol': 'CHF'}
}

# Supported cryptocurrencies
CRYPTOS = {
    'bitcoin': {'symbol': 'BTC', 'name': 'Bitcoin', 'emoji': '₿'},
    'ethereum': {'symbol': 'ETH', 'name': 'Ethereum', 'emoji': '⟠'},
    'binancecoin': {'symbol': 'BNB', 'name': 'Binance Coin', 'emoji': '🟡'},
    'ripple': {'symbol': 'XRP', 'name': 'Ripple', 'emoji': '💧'},
    'cardano': {'symbol': 'ADA', 'name': 'Cardano', 'emoji': '🔵'},
    'dogecoin': {'symbol': 'DOGE', 'name': 'Dogecoin', 'emoji': '🐕'},
    'solana': {'symbol': 'SOL', 'name': 'Solana', 'emoji': '☀️'},
    'polygon': {'symbol': 'MATIC', 'name': 'Polygon', 'emoji': '🟣'}
}

# API URLs
EXCHANGE_API_URL = "https://api.exchangerate-api.com/v4/latest/{}"
CRYPTO_API_URL = "https://api.coingecko.com/api/v3/simple/price"

# Default language
DEFAULT_LANGUAGE = 'tr'