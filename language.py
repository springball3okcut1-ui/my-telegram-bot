# Multi-language support: Turkish, English, Russian
LANGUAGES = {
    'tr': {
        'welcome': '🌟 Para Birimi Botu\'na Hoş Geldiniz! 🌟',
        'select_language': 'Lütfen dilinizi seçin:',
        'language_set': 'Dil Türkçe olarak ayarlandı! 🇹🇷',
        'main_menu': '📊 Ana Menü',
        'currency_rates': '💱 Döviz Kurları',
        'crypto_prices': '₿ Kripto Para Fiyatları',
        'converter': '🔄 Para Çevirici',
        'settings': '⚙️ Ayarlar',
        'current_rates': '📈 Güncel Döviz Kurları',
        'current_crypto': '₿ Güncel Kripto Para Fiyatları',
        'select_from': 'Hangi para biriminden:',
        'select_to': 'Hangi para birimine:',
        'enter_amount': 'Miktarı girin:',
        'conversion_result': '💰 Sonuç: {amount} {from_curr} = {result} {to_curr}',
        'back': '⬅️ Geri',
        'refresh': '🔄 Yenile',
        'error': '❌ Hata oluştu',
        'invalid_amount': '❌ Geçersiz miktar',
        'all_currencies': '🌍 Tüm Para Birimleri',
        'all_cryptos': '₿ Tüm Kripto Paralar'
    },
    'en': {
        'welcome': '🌟 Welcome to Currency Bot! 🌟',
        'select_language': 'Please select your language:',
        'language_set': 'Language set to English! 🇺🇸',
        'main_menu': '📊 Main Menu',
        'currency_rates': '💱 Exchange Rates',
        'crypto_prices': '₿ Crypto Prices',
        'converter': '🔄 Currency Converter',
        'settings': '⚙️ Settings',
        'current_rates': '📈 Current Exchange Rates',
        'current_crypto': '₿ Current Cryptocurrency Prices',
        'select_from': 'Convert from:',
        'select_to': 'Convert to:',
        'enter_amount': 'Enter amount:',
        'conversion_result': '💰 Result: {amount} {from_curr} = {result} {to_curr}',
        'back': '⬅️ Back',
        'refresh': '🔄 Refresh',
        'error': '❌ Error occurred',
        'invalid_amount': '❌ Invalid amount',
        'all_currencies': '🌍 All Currencies',
        'all_cryptos': '₿ All Cryptocurrencies'
    },
    'ru': {
        'welcome': '🌟 Добро пожаловать в Валютный Бот! 🌟',
        'select_language': 'Пожалуйста, выберите язык:',
        'language_set': 'Язык установлен на русский! 🇷🇺',
        'main_menu': '📊 Главное меню',
        'currency_rates': '💱 Курсы валют',
        'crypto_prices': '₿ Цены криптовалют',
        'converter': '🔄 Конвертер валют',
        'settings': '⚙️ Настройки',
        'current_rates': '📈 Текущие курсы валют',
        'current_crypto': '₿ Текущие цены криптовалют',
        'select_from': 'Конвертировать из:',
        'select_to': 'Конвертировать в:',
        'enter_amount': 'Введите сумму:',
        'conversion_result': '💰 Результат: {amount} {from_curr} = {result} {to_curr}',
        'back': '⬅️ Назад',
        'refresh': '🔄 Обновить',
        'error': '❌ Произошла ошибка',
        'invalid_amount': '❌ Неверная сумма',
        'all_currencies': '🌍 Все валюты',
        'all_cryptos': '₿ Все криптовалюты'
    }
}

def get_text(key, lang='tr', **kwargs):
    """Get translated text with parameter substitution"""
    text = LANGUAGES.get(lang, {}).get(key) or LANGUAGES['tr'].get(key, key)
    if text is None:
        return f"Missing translation: {key}"
    return text.format(**kwargs) if kwargs else text

def get_language_options():
    """Get available language options"""
    return {
        'tr': '🇹🇷 Türkçe',
        'en': '🇺🇸 English',
        'ru': '🇷🇺 Русский'
    }