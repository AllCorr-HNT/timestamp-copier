# MyCodex Timestamp Copier v2.0

Małe okienko always-on-top z żywym zegarem.
Jedno kliknięcie = timestamp w schowku.

## Działanie

- **Kliknięcie lewym** na zegar → `Sesja: 30/04/2026 14:15` w schowku
- Okienko zmienia kolor na zielony i pokazuje `✓ Skopiowano!`
- **Prawy klik** → menu (kopiuj / always-on-top toggle / zamknij)
- **Przeciągnij** okienko w dowolne miejsce ekranu

## Wymagania

- Windows 10/11
- Python 3.8+ z opcją "Add Python to PATH"
- Biblioteka: `pyperclip` (instalowana przez INSTALUJ.bat)

## Instalacja

1. Uruchom `INSTALUJ.bat`
2. Okienko pojawi się w prawym dolnym rogu ekranu
3. Opcjonalnie dodaj do autostartu

## Ręczne uruchomienie

```
pythonw timestamp_copier.pyw
```

## Zmiana wersji

### v2.0
- Stałe okienko always-on-top zamiast ikony tray
- Naprawiony schowek (pyperclip zamiast tkinter clipboard)
- Zegar z sekundami (dd/mm/rrrr hh:mm:ss)
- Wizualne potwierdzenie kopiowania (zielone tło)
- Przeciąganie okienka w dowolne miejsce
- Toggle always-on-top przez prawy klik

### v1.0
- Ikona w zasobniku systemowym (tray)
