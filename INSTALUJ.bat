@echo off
title MyCodex Timestamp Copier v2 — Instalator
echo.
echo  ==========================================
echo   MyCodex Timestamp Copier v2 — Instalacja
echo  ==========================================
echo.

REM Sprawdz Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [BLAD] Python nie jest zainstalowany.
    echo  Pobierz ze: https://www.python.org/downloads/
    echo  Zaznacz "Add Python to PATH" podczas instalacji.
    pause
    exit /b 1
)
echo  [OK] Python znaleziony.
echo.

echo  Instalowanie zaleznosci...
pip install pyperclip --quiet
if errorlevel 1 (
    echo  [BLAD] Nie udalo sie zainstalowac pyperclip.
    pause
    exit /b 1
)
echo  [OK] pyperclip zainstalowany.
echo.

set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%timestamp_copier.pyw

echo  Czy dodac do autostartu Windows?
set /p AUTOSTART="  [T/N]: "
if /i "%AUTOSTART%"=="T" (
    set STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    powershell -Command "$ws=New-Object -ComObject WScript.Shell; $s=$ws.CreateShortcut('%STARTUP%\MyCodex Timestamp.lnk'); $s.TargetPath='pythonw.exe'; $s.Arguments='\"%SCRIPT_PATH%\"'; $s.WorkingDirectory='%SCRIPT_DIR%'; $s.Save()"
    echo  [OK] Dodano do autostartu.
)

echo.
echo  Uruchamianie...
start "" pythonw "%SCRIPT_PATH%"

echo.
echo  ==========================================
echo   Gotowe!
echo   Szukaj malego okienka w prawym dolnym
echo   rogu ekranu.
echo.
echo   Kliknij na zegar = kopiuj timestamp
echo   Prawy przycisk   = menu
echo   Przeciagnij      = przesuń okienko
echo  ==========================================
echo.
pause
