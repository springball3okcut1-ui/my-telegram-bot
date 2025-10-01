#!/usr/bin/env python3
"""
Bot Auto-Restart Script
Bot durduğunda otomatik olarak yeniden başlatır
"""

import subprocess
import time
import os
import sys
from datetime import datetime

def log_message(message):
    """Log mesajı yazdır"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def start_bot():
    """Botu başlat"""
    try:
        log_message("🤖 Bot başlatılıyor...")
        
        # Bot dizinine git
        os.chdir(r"C:\Users\STORMBEAT\OneDrive - ADMIU\Belgeler")
        
        # Botu başlat
        process = subprocess.Popen([sys.executable, "currency_bot.py"])
        
        log_message(f"✅ Bot başlatıldı! PID: {process.pid}")
        return process
        
    except Exception as e:
        log_message(f"❌ Bot başlatılamadı: {e}")
        return None

def monitor_bot():
    """Botu izle ve gerektiğinde yeniden başlat"""
    process = None
    restart_count = 0
    
    while True:
        try:
            # Bot çalışmıyorsa başlat
            if process is None or process.poll() is not None:
                if process is not None:
                    restart_count += 1
                    log_message(f"🔄 Bot durdu! Yeniden başlatılıyor... (Sayı: {restart_count})")
                
                process = start_bot()
                
                if process is None:
                    log_message("⏳ 10 saniye sonra tekrar denenecek...")
                    time.sleep(10)
                    continue
            
            # Bot çalışıyor, 30 saniye bekle
            time.sleep(30)
            
        except KeyboardInterrupt:
            log_message("🛑 Bot izleyicisi durduruluyor...")
            if process:
                process.terminate()
            break
        except Exception as e:
            log_message(f"❌ Hata: {e}")
            time.sleep(10)

if __name__ == "__main__":
    log_message("🚀 Bot Auto-Restart Script başlatıldı!")
    log_message("💡 Bot durduğunda otomatik olarak yeniden başlatılacak")
    log_message("🛑 Durdurmak için Ctrl+C basın")
    
    monitor_bot()






