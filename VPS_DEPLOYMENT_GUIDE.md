# Currency Bot VPS Deployment Guide

## 🚀 VPS'te Bot Kurulumu

### 1. VPS'e Bağlanma
```bash
ssh root@your-vps-ip
```

### 2. Deployment Script'ini Çalıştırma
```bash
# Script'i indir ve çalıştır
wget https://your-domain.com/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

### 3. Manuel Kurulum (Alternatif)

#### Sistem Güncellemesi
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv -y
```

#### Proje Dizini Oluşturma
```bash
mkdir -p /opt/currency_bot
cd /opt/currency_bot
```

#### Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
pip install python-telegram-bot requests
```

#### Bot Dosyalarını Yükleme
```bash
# currency_bot.py dosyasını VPS'e yükleyin
# requirements.txt dosyasını VPS'e yükleyin

# Örnek: SCP ile dosya yükleme
scp currency_bot.py root@your-vps-ip:/opt/currency_bot/
scp requirements.txt root@your-vps-ip:/opt/currency_bot/
```

### 4. Systemd Service Oluşturma

```bash
sudo nano /etc/systemd/system/currency-bot.service
```

Service dosyası içeriği:
```ini
[Unit]
Description=Currency Exchange Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/currency_bot
Environment=PATH=/opt/currency_bot/venv/bin
ExecStart=/opt/currency_bot/venv/bin/python /opt/currency_bot/currency_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 5. Service'i Başlatma

```bash
sudo systemctl daemon-reload
sudo systemctl enable currency-bot
sudo systemctl start currency-bot
```

### 6. Bot Durumunu Kontrol Etme

```bash
# Bot durumu
sudo systemctl status currency-bot

# Bot logları
sudo journalctl -u currency-bot -f

# Bot çalışıyor mu?
sudo systemctl is-active currency-bot
```

## 🔧 Yönetim Komutları

### Bot Kontrolü
```bash
# Botu başlat
sudo systemctl start currency-bot

# Botu durdur
sudo systemctl stop currency-bot

# Botu yeniden başlat
sudo systemctl restart currency-bot

# Bot durumunu kontrol et
sudo systemctl status currency-bot
```

### Log Takibi
```bash
# Canlı log takibi
sudo journalctl -u currency-bot -f

# Son 100 log satırı
sudo journalctl -u currency-bot -n 100

# Belirli tarih aralığındaki loglar
sudo journalctl -u currency-bot --since "2024-01-01" --until "2024-01-02"
```

### Bot Güncelleme
```bash
# Botu durdur
sudo systemctl stop currency-bot

# Yeni dosyaları yükle
scp currency_bot.py root@your-vps-ip:/opt/currency_bot/

# Botu yeniden başlat
sudo systemctl start currency-bot
```

## 🛡️ Güvenlik ve Optimizasyon

### Firewall Ayarları
```bash
# UFW firewall kurulumu
sudo apt install ufw -y
sudo ufw enable

# SSH portunu aç
sudo ufw allow 22

# Gerekli portları aç (bot için port gerekmez)
sudo ufw status
```

### Otomatik Backup
```bash
# Backup script oluştur
sudo nano /opt/backup_bot.sh
```

Backup script içeriği:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf /opt/backups/currency_bot_$DATE.tar.gz /opt/currency_bot/
find /opt/backups/ -name "currency_bot_*.tar.gz" -mtime +7 -delete
```

### Cron Job ile Otomatik Backup
```bash
# Crontab düzenle
sudo crontab -e

# Her gün saat 02:00'da backup al
0 2 * * * /opt/backup_bot.sh
```

## 📊 Monitoring

### Bot Sağlık Kontrolü
```bash
# Bot çalışıyor mu?
curl -s http://localhost:8080/health || echo "Bot çalışmıyor"

# Sistem kaynakları
htop
df -h
free -h
```

### Log Rotation
```bash
# Logrotate ayarları
sudo nano /etc/logrotate.d/currency-bot
```

Logrotate içeriği:
```
/var/log/currency-bot.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 root root
    postrotate
        systemctl reload currency-bot
    endscript
}
```

## 🚨 Sorun Giderme

### Bot Çalışmıyor
```bash
# Logları kontrol et
sudo journalctl -u currency-bot -n 50

# Python path kontrolü
which python3
/opt/currency_bot/venv/bin/python --version

# Dosya izinleri
ls -la /opt/currency_bot/
```

### Port Çakışması
```bash
# Kullanılan portları kontrol et
netstat -tulpn | grep :8080
lsof -i :8080
```

### Memory Kullanımı
```bash
# Memory kullanımını kontrol et
ps aux | grep currency_bot
free -h
```

## 📱 Telegram Bot Test

Botunuz çalıştıktan sonra Telegram'da test edin:
1. Botunuzu bulun
2. `/start` komutunu gönderin
3. Dil seçimi yapın
4. Para birimi dönüşümü test edin

## 🔄 Otomatik Yeniden Başlatma

Bot otomatik olarak yeniden başlatılacak çünkü systemd service'inde `Restart=always` ayarı var. Bot çökerse 10 saniye sonra otomatik olarak yeniden başlar.







