@echo off
echo Telegram Currency Bot - Windows Servisi Kurulumu
echo.

REM Bot dizinine git
cd /d "C:\Users\STORMBEAT\OneDrive - ADMIU\Belgeler"

REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo Python bulunamadi! Lutfen Python'u yukleyin.
    pause
    exit /b 1
)

REM Botu başlat
echo Bot baslatiliyor...
python currency_bot.py

REM Hata durumunda bekle
if errorlevel 1 (
    echo Bot durdu! 5 saniye sonra yeniden baslatiliyor...
    timeout /t 5 /nobreak >nul
    goto :start
)

:start
python currency_bot.py
goto :start






