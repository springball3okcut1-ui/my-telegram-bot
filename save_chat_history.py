#!/usr/bin/env python3
"""
Chat History Saver
Bu script chat geçmişini otomatik olarak kaydeder
"""

import os
from datetime import datetime

def save_chat_history():
    """Chat geçmişini kaydet"""
    
    # Mevcut tarih ve saat
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    
    # Chat geçmişi içeriği
    chat_content = f"""
# Telegram Currency Bot - Chat History
# Kayıt Tarihi: {now.strftime("%Y-%m-%d %H:%M:%S")}

## Bot Özellikleri:
- 6 Fiat Para Birimi (TRY, AZN, RUB, USD, EUR, GBP)
- 50+ Kripto Para (BTC, ETH, BNB, ADA, SOL, XRP, DOT, DOGE, MATIC, AVAX, vb.)
- 3 Dil Desteği (Türkçe, İngilizce, Rusça)
- Direkt Metin Girişi (örn: "20 USD TRY")
- İnteraktif Menüler
- 3000+ Para Birimi Kombinasyonu

## Dosyalar:
- currency_bot.py (Ana bot kodu)
- requirements.txt (Python bağımlılıkları)
- README.md (Kullanım kılavuzu)
- VPS_DEPLOYMENT_GUIDE.md (VPS kurulum rehberi)
- systemd_service.md (Servis kurulumu)
- deploy.sh (Otomatik kurulum scripti)
- vps_setup.sh (VPS kurulum scripti)

## API'ler:
- ExchangeRate-API: Ücretsiz, günlük 1,500 istek
- CoinGecko API: Ücretsiz, günlük 10,000 istek
- Telegram Bot API: Ücretsiz, sınırsız

## Özellikler:
✅ Çoklu dil desteği
✅ Fiat para birimi dönüşümü
✅ Kripto para dönüşümü
✅ Direkt metin girişi
✅ İnteraktif menüler
✅ Emoji'li butonlar
✅ Otomatik dil seçimi
✅ Hata yönetimi
✅ Logging sistemi

## Kullanım:
1. Botu başlatın: py currency_bot.py
2. Telegram'da botunuzu bulun
3. /start komutu ile başlayın
4. Dil seçin (TR/EN/RU)
5. Para birimi karşılaştırması yapın
6. Direkt metin girişi kullanın (örn: "100 BTC TRY")

## VPS Kurulumu:
- Ubuntu/Debian VPS gerekli
- Python 3.8+ gerekli
- systemd servisi ile otomatik başlatma
- Otomatik yeniden başlatma
- Log dosyaları

## Notlar:
- Bot tamamen ücretsiz
- API'ler ücretsiz
- Sınırsız kullanım
- 7/24 çalışabilir
- VPS'te host edilebilir

# Chat History End
"""
    
    # Dosya adı
    filename = f"chat_history_{timestamp}.txt"
    
    # Dosyayı kaydet
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(chat_content)
        
        print(f"✅ Chat geçmişi kaydedildi: {filename}")
        print(f"📁 Konum: {os.path.abspath(filename)}")
        
        return filename
        
    except Exception as e:
        print(f"❌ Hata: {e}")
        return None

if __name__ == "__main__":
    save_chat_history()







