@echo off
title CRSL MONITOR

echo ========================================
echo          CRSL MONITOR SYSTEM
echo ========================================
echo.

cd /d "D:\Praktik Scripting Language\CRSL-Monitor"

echo Mengaktifkan Telegram Bot...
start "CRSL Telegram Bot" cmd /k "call venv\Scripts\activate.bat && python bot.py"

timeout /t 3 /nobreak >nul

echo Mengaktifkan Dashboard Flask...
start "CRSL Dashboard" cmd /k "call venv\Scripts\activate.bat && python app.py"

timeout /t 3 /nobreak >nul

echo Mengaktifkan Scheduler...
start "CRSL Scheduler" cmd /k "call venv\Scripts\activate.bat && python scheduler.py"

echo.
echo ========================================
echo SEMUA KOMPONEN CRSL MONITOR DIAKTIFKAN
echo ========================================
echo.
pause