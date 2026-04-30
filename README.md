# MyCodex Timestamp Copier

Aplikacja w zasobniku systemowym (system tray) która jednym kliknięciem
kopiuje aktualny timestamp sesji do schowka.

## Działanie

- **Lewy klik** ikony → timestamp w schowku + toast z potwierdzeniem
- **Prawy klik** → menu (Kopiuj / Zamknij)
- Format: `Sesja: 30/04/2026 14:15`

## Wymagania

- Windows 10/11
- Python 3.8+ (https://python.org) — zaznacz "Add Python to PATH"
- Biblioteki: `pystray`, `pillow` (instalowane automatycznie przez INSTALUJ.bat)

## Instalacja

1. Uruchom `INSTALUJ.bat` jako zwykły użytkownik (nie Administrator)
2. Opcjonalnie zaznacz autostart przy starcie Windows
3. Ikona pojawi się w zasobniku (prawy dolny róg, może być ukryta — kliknij strzałkę ^)

## Przypięcie do paska zadań

Windows nie pozwala przypiąć aplikacji tray bezpośrednio do paska.
Najwygodniejsze rozwiązanie:

1. Prawym na `timestamp_copier.pyw` → Wyślij do → Pulpit (utwórz skrót)
2. Skrót można przeciągnąć do paska szybkiego uruchamiania (Quick Launch)
   lub trzymać na pulpicie

## Ręczne uruchomienie

```
pythonw timestamp_copier.pyw
```

## Odinstalowanie

Zamknij przez prawy klik → Zamknij, usuń folder.
Jeśli dodano autostart: usuń skrót z:
`C:\Users\[użytkownik]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
