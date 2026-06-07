"""
MyCodex Timestamp Copier v2.1
==============================
Małe okienko always-on-top z żywym zegarem.
Kliknięcie na zegar → timestamp w schowku.
Prawy przycisk → menu (przypnij / zamknij).

Wymagania: pip install pyperclip
"""

import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime
import pyperclip
import sys


# ── Konfiguracja wyglądu ──────────────────────────────────────────────────────

BG_NORMAL   = '#1e1b4b'
BG_HOVER    = '#4c1d95'
BG_CLICK    = '#7c3aed'
BG_COPIED   = '#065f46'
FG_CLOCK    = '#e2d4f8'
FG_COPIED   = '#6ee7b7'
FG_HINT     = '#a78bfa'
ALPHA       = 0.92


# ── Pomocnicze ────────────────────────────────────────────────────────────────

def get_timestamp() -> str:
    """Sesja: rrrr/mm/dd hh:mm"""
    now = datetime.now()
    return f"Sesja: {now.strftime('%Y/%m/%d %H:%M')}"


def get_clock() -> str:
    """rrrr/mm/dd  hh:mm:ss"""
    now = datetime.now()
    return now.strftime('%Y/%m/%d   %H:%M:%S')


# ── Główna aplikacja ──────────────────────────────────────────────────────────

class TimestampApp:
    DRAG_THRESHOLD = 5

    def __init__(self) -> None:
        self.root = tk.Tk()
        self._setup_window()
        self._build_ui()
        self._bind_events()
        self._tick()

    def _setup_window(self) -> None:
        root = self.root
        root.title('MyCodex Timestamp')
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-alpha', ALPHA)
        root.configure(bg=BG_NORMAL)
        root.resizable(False, False)
        root.update_idletasks()
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        root.geometry(f'+{sw - 280}+{sh - 120}')

    def _build_ui(self) -> None:
        root = self.root

        self.frame = tk.Frame(root, bg=BG_NORMAL, cursor='hand2')
        self.frame.pack(fill='both', expand=True, padx=0, pady=0)

        self.title_bar = tk.Frame(self.frame, bg=BG_NORMAL)
        self.title_bar.pack(fill='x', padx=12, pady=(10, 2))

        tk.Label(
            self.title_bar, text='●',
            fg='#7c3aed', bg=BG_NORMAL, font=('Segoe UI', 8),
        ).pack(side='left')

        tk.Label(
            self.title_bar, text='  MyCodex',
            fg=FG_HINT, bg=BG_NORMAL, font=('Segoe UI', 8),
        ).pack(side='left')

        self.close_btn = tk.Label(
            self.title_bar, text='✕',
            fg=FG_HINT, bg=BG_NORMAL,
            font=('Segoe UI', 9), cursor='hand2',
        )
        self.close_btn.pack(side='right')
        self.close_btn.bind('<Button-1>', lambda e: self.root.destroy())

        self.clock_lbl = tk.Label(
            self.frame,
            text='',
            fg=FG_CLOCK,
            bg=BG_NORMAL,
            font=('Courier New', 15, 'bold'),
            cursor='hand2',
            padx=16,
            pady=4,
        )
        self.clock_lbl.pack(fill='x')

        self.hint_lbl = tk.Label(
            self.frame,
            text='kliknij → kopiuj  •  PPM → menu',
            fg=FG_HINT,
            bg=BG_NORMAL,
            font=('Segoe UI', 7),
            pady=(0),
            padx=16,
        )
        self.hint_lbl.pack(fill='x', pady=(0, 10))

        tk.Frame(self.frame, bg='#4c1d95', height=2).pack(fill='x', side='bottom')

    def _bind_events(self) -> None:
        for widget in (self.frame, self.clock_lbl, self.hint_lbl):
            widget.bind('<Enter>',           self._on_hover)
            widget.bind('<Leave>',           self._on_leave)
            widget.bind('<ButtonPress-1>',   self._on_press)
            widget.bind('<B1-Motion>',       self._on_drag)
            widget.bind('<ButtonRelease-1>', self._on_release)
            widget.bind('<Button-3>',        self._on_right_click)

        self.title_bar.bind('<ButtonPress-1>',   self._on_press)
        self.title_bar.bind('<B1-Motion>',       self._on_drag)
        self.title_bar.bind('<ButtonRelease-1>', self._on_drag_release)

        self._drag_start_x = 0
        self._drag_start_y = 0
        self._drag_win_x   = 0
        self._drag_win_y   = 0
        self._dragging     = False
        self._press_x      = 0
        self._press_y      = 0

    def _on_hover(self, event) -> None:
        self._set_bg(BG_HOVER)

    def _on_leave(self, event) -> None:
        self._set_bg(BG_NORMAL)

    def _on_press(self, event) -> None:
        self._press_x      = event.x_root
        self._press_y      = event.y_root
        self._drag_start_x = event.x_root
        self._drag_start_y = event.y_root
        self._drag_win_x   = self.root.winfo_x()
        self._drag_win_y   = self.root.winfo_y()
        self._dragging     = False
        self._set_bg(BG_CLICK)

    def _on_drag(self, event) -> None:
        dx = abs(event.x_root - self._press_x)
        dy = abs(event.y_root - self._press_y)
        if dx > self.DRAG_THRESHOLD or dy > self.DRAG_THRESHOLD:
            self._dragging = True
            new_x = self._drag_win_x + (event.x_root - self._drag_start_x)
            new_y = self._drag_win_y + (event.y_root - self._drag_start_y)
            self.root.geometry(f'+{new_x}+{new_y}')

    def _on_drag_release(self, event) -> None:
        self._set_bg(BG_NORMAL)

    def _on_release(self, event) -> None:
        if not self._dragging:
            self._copy_timestamp()
        else:
            self._set_bg(BG_NORMAL)
        self._dragging = False

    def _on_right_click(self, event) -> None:
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label='Kopiuj timestamp',  command=self._copy_timestamp)
        menu.add_separator()
        menu.add_command(label='Zawsze na wierzchu — ON',
                         command=lambda: self.root.attributes('-topmost', True))
        menu.add_command(label='Zawsze na wierzchu — OFF',
                         command=lambda: self.root.attributes('-topmost', False))
        menu.add_separator()
        menu.add_command(label='Zamknij', command=self.root.destroy)
        menu.tk_popup(event.x_root, event.y_root)

    def _copy_timestamp(self) -> None:
        ts = get_timestamp()
        try:
            pyperclip.copy(ts)
        except Exception:
            self.root.clipboard_clear()
            self.root.clipboard_append(ts)
            self.root.update()

        self._set_bg(BG_COPIED)
        self.clock_lbl.config(fg=FG_COPIED)
        self.hint_lbl.config(
            text=f'✓ Skopiowano!   {ts}',
            fg=FG_COPIED,
        )
        self.root.after(1500, self._reset_after_copy)

    def _reset_after_copy(self) -> None:
        self._set_bg(BG_NORMAL)
        self.clock_lbl.config(fg=FG_CLOCK)
        self.hint_lbl.config(
            text='kliknij → kopiuj  •  PPM → menu',
            fg=FG_HINT,
        )

    def _tick(self) -> None:
        self.clock_lbl.config(text=get_clock())
        self.root.after(1000, self._tick)

    def _set_bg(self, color: str) -> None:
        self.root.configure(bg=color)
        for w in (self.frame, self.clock_lbl, self.hint_lbl, self.title_bar):
            w.configure(bg=color)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == '__main__':
    app = TimestampApp()
    app.run()