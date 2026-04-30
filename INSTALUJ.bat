@echo off
title MyCodex Timestamp Copier — Instalator
echo.
echo  ========================================
echo   MyCodex Timestamp Copier — Instalacja
echo  ========================================
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
pip install pystray pillow --quiet

if errorlevel 1 (
    echo  [BLAD] Nie udalo sie zainstalowac zaleznosci.
    pause
    exit /b 1
)

echo  [OK] Zaleznosci zainstalowane.
echo.

REM Ustal pelna sciezke do skryptu
set SCRIPT_DIR=%~dp0
set SCRIPT_PATH=%SCRIPT_DIR%timestamp_copier.pyw

REM Stworz skrot w folderze Startup (autostart) — opcjonalnie
echo  Czy dodac do autostartu Windows? (uruchomi sie przy starcie systemu)
set /p AUTOSTART="  [T/N]: "
if /i "%AUTOSTART%"=="T" (
    set STARTUP_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
    powershell -Command "$ws = New-Object -ComObject WScript.Shell; $s = $ws.CreateShortcut('%STARTUP_DIR%\MyCodex Timestamp.lnk'); $s.TargetPath = 'pythonw.exe'; $s.Arguments = '\"%SCRIPT_PATH%\"'; $s.WorkingDirectory = '%SCRIPT_DIR%'; $s.Description = 'MyCodex Timestamp Copier'; $s.Save()"
    echo  [OK] Dodano do autostartu.
)

echo.
echo  Uruchamianie aplikacji...
start "" pythonw "%SCRIPT_PATH%"

echo.
echo  ========================================
echo   Gotowe! Ikona pojawila sie w zasobniku.
echo   Kliknij lewy przycisk = kopiuj timestamp
echo   Kliknij prawy przycisk = menu / zamknij
echo  ========================================
echo.
pause
