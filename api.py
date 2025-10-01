import requests
import json
from datetime import datetime
from config import CURRENCIES, CRYPTOS, EXCHANGE_API_URL, CRYPTO_API_URL
from language import get_text

class CurrencyAPI:
    """Handle currency and cryptocurrency API requests"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Currency Bot/1.0'
        })
    
    def get_exchange_rates(self, base='USD'):
        """Get current exchange rates"""
        try:
            url = EXCHANGE_API_URL.format(base)
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data.get('rates', {})
        except Exception as e:
            print(f"Exchange rate API error: {e}")
            return {}
    
    def convert_currency(self, amount, from_curr, to_curr):
        """Convert currency"""
        if from_curr == to_curr:
            return amount
        
        try:
            rates = self.get_exchange_rates(from_curr)
            if to_curr in rates:
                return round(amount * rates[to_curr], 2)
        except Exception as e:
            print(f"Currency conversion error: {e}")
        
        return None
    
    def get_formatted_rates(self, lang='tr'):
        """Get formatted currency rates text"""
        rates = self.get_exchange_rates('USD')
        
        if not rates:
            return get_text('error', lang)
        
        text = f"{get_text('current_rates', lang)} (USD)\n\n"
        
        for code, info in CURRENCIES.items():
            if code in rates:
                rate = f"{rates[code]:.4f}"
                text += f"{info['flag']} 1 USD = {rate} {code}\n"
        
        text += f"\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        return text
    
    def get_crypto_prices(self, crypto_list=None):
        """Get cryptocurrency prices"""
        try:
            if crypto_list:
                crypto_ids = ','.join(crypto_list)
            else:
                crypto_ids = ','.join(CRYPTOS.keys())
                
            params = {
                'ids': crypto_ids,
                'vs_currencies': 'usd,eur,try',
                'include_24hr_change': 'true'
            }
            
            response = self.session.get(CRYPTO_API_URL, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Crypto API error: {e}")
            return {}
    
    def get_formatted_crypto_prices(self, lang='tr'):
        """Get formatted crypto prices text"""
        prices = self.get_crypto_prices()
        
        if not prices:
            return get_text('error', lang)
        
        text = f"{get_text('current_crypto', lang)} (USD)\n\n"
        
        for crypto_id, info in CRYPTOS.items():
            if crypto_id in prices:
                price_data = prices[crypto_id]
                price = f"{price_data['usd']:.2f}"
                change = price_data.get('usd_24h_change', 0)
                change_str = f"{change:+.2f}"
                emoji = '📈' if change >= 0 else '📉'
                
                text += f"{info['emoji']} {info['symbol']}: ${price} ({emoji} {change_str}%)\n"
        
        text += f"\n🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        return text
    
    def convert_crypto_to_fiat(self, amount, crypto_symbol, fiat_currency='USD'):
        """Convert cryptocurrency to fiat currency"""
        try:
            # Find crypto ID by symbol
            crypto_id = None
            for cid, info in CRYPTOS.items():
                if info['symbol'].upper() == crypto_symbol.upper():
                    crypto_id = cid
                    break
            
            if not crypto_id:
                return None
            
            prices = self.get_crypto_prices()
            if crypto_id not in prices:
                return None
            
            usd_price = prices[crypto_id]['usd']
            usd_value = amount * usd_price
            
            if fiat_currency.upper() == 'USD':
                return round(usd_value, 2)
            
            # Convert USD to target fiat currency
            return self.convert_currency(usd_value, 'USD', fiat_currency.upper())
            
        except Exception as e:
            print(f"Crypto conversion error: {e}")
            return None