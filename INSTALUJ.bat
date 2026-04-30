@echo off
chcp 65001 >nul
title MyCodex Timestamp Copier v2 - Instalator
echo.
echo  ==========================================
echo   MyCodex Timestamp Copier v2 - Instalacja
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
pip install pyperclip --quiet --disable-pip-version-check
if errorlevel 1 (
    echo  [BLAD] Nie udalo sie zainstalowac pyperclip.
    pause
    exit /b 1
)
echo  [OK] pyperclip zainstalowany.
echo.

set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%~dp0timestamp_copier.pyw"
set "STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT=%STARTUP_DIR%\MyCodex Timestamp.lnk"
set "PS_TEMP=%TEMP%\mycodex_shortcut.ps1"

echo  Czy dodac do autostartu Windows?
set /p AUTOSTART="  [T/N]: "

if /i "%AUTOSTART%"=="T" (
    (
        echo $ws = New-Object -ComObject WScript.Shell
        echo $s = $ws.CreateShortcut('%SHORTCUT%'^)
        echo $s.TargetPath = 'pythonw.exe'
        echo $s.Arguments = '"%SCRIPT_PATH%"'
        echo $s.WorkingDirectory = '%SCRIPT_DIR%'
        echo $s.Description = 'MyCodex Timestamp Copier'
        echo $s.Save(^)
    ) > "%PS_TEMP%"

    powershell -ExecutionPolicy Bypass -File "%PS_TEMP%"

    if exist "%SHORTCUT%" (
        echo  [OK] Dodano do autostartu.
    ) else (
        echo  [UWAGA] Nie udalo sie dodac do autostartu.
        echo          Mozesz recznie umiescic skrot w:
        echo          %STARTUP_DIR%
    )
    del "%PS_TEMP%" >nul 2>&1
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
echo   Klik lewy   = kopiuj timestamp
echo   Klik prawy  = menu
echo   Przeciagnij = przesun okienko
echo  ==========================================
echo.
pause
