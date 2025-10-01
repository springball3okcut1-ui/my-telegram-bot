# Currency Bot VPS Service Configuration

## Systemd Service Dosyası

Bu dosyayı `/etc/systemd/system/currency-bot.service` olarak kaydedin:

```ini
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
```

## Service Yönetimi

### Service'i Etkinleştirme
```bash
sudo systemctl daemon-reload
sudo systemctl enable currency-bot
sudo systemctl start currency-bot
```

### Service Durumu Kontrolü
```bash
# Service durumu
sudo systemctl status currency-bot

# Service aktif mi?
sudo systemctl is-active currency-bot

# Service etkin mi?
sudo systemctl is-enabled currency-bot
```

### Service Kontrol Komutları
```bash
# Başlat
sudo systemctl start currency-bot

# Durdur
sudo systemctl stop currency-bot

# Yeniden başlat
sudo systemctl restart currency-bot

# Reload (config değişiklikleri için)
sudo systemctl reload currency-bot
```

## Log Yönetimi

### Log Görüntüleme
```bash
# Canlı log takibi
sudo journalctl -u currency-bot -f

# Son 50 log satırı
sudo journalctl -u currency-bot -n 50

# Belirli tarihten itibaren
sudo journalctl -u currency-bot --since "2024-01-01"

# Hata logları
sudo journalctl -u currency-bot -p err
```

### Log Temizleme
```bash
# Eski logları temizle
sudo journalctl --vacuum-time=7d

# Log boyutunu sınırla
sudo journalctl --vacuum-size=100M
```

## Otomatik Başlatma

Service dosyasında `WantedBy=multi-user.target` ayarı sayesinde bot sistem açılışında otomatik olarak başlar.

## Güvenlik Ayarları

Service dosyasında güvenlik için:
- `NoNewPrivileges=true`: Yeni ayrıcalık kazanımını engeller
- `PrivateTmp=true`: Geçici dosyaları izole eder
- `ProtectSystem=strict`: Sistem dosyalarını korur
- `ProtectHome=true`: Home dizinini korur
- `ReadWritePaths=/opt/currency_bot`: Sadece bot dizinine yazma izni

## Monitoring ve Alerting

### Health Check Script
```bash
#!/bin/bash
# /opt/health_check.sh

if ! systemctl is-active --quiet currency-bot; then
    echo "Currency bot is not running!"
    systemctl start currency-bot
    # Email gönder veya webhook çağır
fi
```

### Cron Job ile Health Check
```bash
# Her 5 dakikada bir kontrol et
*/5 * * * * /opt/health_check.sh
```

## Backup ve Restore

### Backup Script
```bash
#!/bin/bash
# /opt/backup_bot.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/backups"
BOT_DIR="/opt/currency_bot"

mkdir -p $BACKUP_DIR

# Bot dosyalarını yedekle
tar -czf $BACKUP_DIR/currency_bot_$DATE.tar.gz $BOT_DIR/

# Eski yedekleri sil (7 günden eski)
find $BACKUP_DIR -name "currency_bot_*.tar.gz" -mtime +7 -delete

echo "Backup completed: currency_bot_$DATE.tar.gz"
```

### Restore Script
```bash
#!/bin/bash
# /opt/restore_bot.sh

BACKUP_FILE=$1
BOT_DIR="/opt/currency_bot"

if [ -z "$BACKUP_FILE" ]; then
    echo "Usage: $0 <backup_file.tar.gz>"
    exit 1
fi

# Botu durdur
systemctl stop currency-bot

# Mevcut dosyaları yedekle
mv $BOT_DIR $BOT_DIR.backup.$(date +%Y%m%d_%H%M%S)

# Yedekten geri yükle
tar -xzf $BACKUP_FILE -C /

# Botu başlat
systemctl start currency-bot

echo "Restore completed from $BACKUP_FILE"
```

## Performance Monitoring

### Resource Usage Monitoring
```bash
# CPU ve Memory kullanımı
ps aux | grep currency_bot

# Disk kullanımı
df -h /opt/currency_bot

# Network bağlantıları
netstat -tulpn | grep python
```

### Log Analysis
```bash
# Hata sayısı
sudo journalctl -u currency-bot --since "1 hour ago" | grep -i error | wc -l

# Başarılı istekler
sudo journalctl -u currency-bot --since "1 hour ago" | grep "HTTP/1.1 200" | wc -l
```

Bu konfigürasyon ile botunuz VPS'te güvenli ve kararlı bir şekilde çalışacaktır.







