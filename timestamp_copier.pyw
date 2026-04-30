"""
MyCodex Timestamp Copier
========================
Kliknij ikonę w pasku zadań → timestamp w schowku.
Prawy przycisk → menu z opcjami.

Wymagania: pip install pystray pillow
"""

import pystray
import threading
from PIL import Image, ImageDraw
from datetime import datetime
import tkinter as tk
import sys
import os


def get_timestamp() -> str:
    """Zwraca aktualny timestamp w formacie: Sesja: dd/mm/rrrr hh:mm"""
    now = datetime.now()
    return f"Sesja: {now.strftime('%d/%m/%Y %H:%M')}"


def copy_to_clipboard(text: str) -> None:
    """Kopiuje tekst do schowka przez tkinter (bez otwierania okna)."""
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    # Musimy utrzymać root przy życiu chwilę żeby schowek nie zginął
    root.after(3000, root.destroy)
    root.mainloop()


def show_toast(message: str) -> None:
    """Wyświetla minimalne okienko toast które znika po 2 sekundach."""
    toast = tk.Tk()
    toast.overrideredirect(True)  # Brak ramki i paska tytułu
    toast.attributes('-topmost', True)
    toast.attributes('-alpha', 0.92)
    toast.configure(bg='#1e1b4b')

    label = tk.Label(
        toast,
        text=message,
        font=('Segoe UI', 10),
        fg='#e2d4f8',
        bg='#1e1b4b',
        padx=18,
        pady=10,
    )
    label.pack()

    # Pozycjonuj w prawym dolnym rogu (nad paskiem zadań)
    toast.update_idletasks()
    w = toast.winfo_width()
    h = toast.winfo_height()
    screen_w = toast.winfo_screenwidth()
    screen_h = toast.winfo_screenheight()
    x = screen_w - w - 20
    y = screen_h - h - 60
    toast.geometry(f'+{x}+{y}')

    toast.after(2000, toast.destroy)
    toast.mainloop()


def on_click_copy(icon, item=None) -> None:
    """Główna akcja: kopiuj timestamp + pokaż toast."""
    ts = get_timestamp()

    # Kopiuj w osobnym wątku (tkinter wymaga własnego mainloop)
    copy_thread = threading.Thread(target=copy_to_clipboard, args=(ts,), daemon=True)
    copy_thread.start()
    copy_thread.join()

    # Toast w osobnym wątku
    toast_thread = threading.Thread(target=show_toast, args=(f'✓ {ts}',), daemon=True)
    toast_thread.start()


def on_quit(icon, item) -> None:
    """Zamknij aplikację."""
    icon.stop()


def create_icon_image() -> Image.Image:
    """
    Tworzy ikonę 64x64 — fioletowe kółko z białą literą S (Session).
    Galaxy theme.
    """
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Tło — fioletowe kółko
    margin = 2
    draw.ellipse(
        [margin, margin, size - margin, size - margin],
        fill='#7c3aed',
    )

    # Litera S w środku
    try:
        from PIL import ImageFont
        font = ImageFont.truetype('segoeui.ttf', 30)
    except Exception:
        font = ImageFont.load_default()

    text = 'S'
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    x = (size - text_w) / 2 - bbox[0]
    y = (size - text_h) / 2 - bbox[1]
    draw.text((x, y), text, fill='white', font=font)

    return img


def build_menu() -> pystray.Menu:
    """Buduje menu prawego przycisku myszy."""
    return pystray.Menu(
        pystray.MenuItem(
            'Kopiuj timestamp sesji',
            on_click_copy,
            default=True,  # Akcja domyślna = lewy klik
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Zamknij', on_quit),
    )


def main() -> None:
    icon_image = create_icon_image()
    ts_preview = get_timestamp()

    icon = pystray.Icon(
        name='MyCodex Timestamp',
        icon=icon_image,
        title=f'MyCodex · {ts_preview}',
        menu=build_menu(),
    )

    # Lewy klik = kopiuj (pystray obsługuje przez default=True w MenuItem)
    icon.run()


if __name__ == '__main__':
    main()
