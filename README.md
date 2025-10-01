# Currency Exchange Bot

Bu Telegram botu Türkiye, Azerbaycan, Rusya, Amerika ve Avrupa para birimlerinin güncel kurlarını gösterir ve para birimi karşılaştırması yapabilir. Ayrıca kripto para kurlarını da destekler.

## Özellikler

- 🇹🇷 Türkçe, 🇺🇸 İngilizce ve 🇷🇺 Rusça dil desteği
- Güncel döviz kurları (TRY, AZN, RUB, USD, EUR, GBP)
- Kripto para kurları (BTC, ETH, BNB, ADA, SOL)
- Para birimi karşılaştırması
- İnteraktif butonlar ve menüler
- Gerçek zamanlı kur güncellemeleri

## Kurulum

1. Python 3.8+ yüklü olduğundan emin olun
2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Bot token'ınızı `currency_bot.py` dosyasında güncelleyin:
```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
```

4. Botu çalıştırın:
```bash
python currency_bot.py
```

## Kullanım

1. Telegram'da botunuzu bulun ve `/start` komutunu gönderin
2. Ana menüden istediğiniz özelliği seçin:
   - **Güncel Kurlar**: Tüm para birimlerinin güncel kurlarını görün
   - **Para Birimi Karşılaştırması**: İki para birimi arasında dönüşüm yapın
   - **Kripto Para Kurları**: Kripto para kurlarını görün
   - **Dil Seçimi**: Bot dilini değiştirin

## API'ler

Bot aşağıdaki ücretsiz API'leri kullanır:
- ExchangeRate-API: Döviz kurları için
- CoinGecko API: Kripto para kurları için

## Desteklenen Para Birimleri

### Fiat Para Birimleri
- TRY (Türk Lirası)
- AZN (Azerbaycan Manatı)
- RUB (Rus Rublesi)
- USD (Amerikan Doları)
- EUR (Euro)
- GBP (İngiliz Sterlini)

### Kripto Para Birimleri
- BTC (Bitcoin)
- ETH (Ethereum)
- BNB (Binance Coin)
- ADA (Cardano)
- SOL (Solana)

## Geliştirme

Bot Python 3.8+ ile yazılmıştır ve python-telegram-bot kütüphanesini kullanır.

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır.







