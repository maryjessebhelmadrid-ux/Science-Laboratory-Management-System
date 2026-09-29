import tkinter as tk

class RoundClickableLabel(tk.Canvas):
    def __init__(self, parent, text, radius, bg_color, text_color, border_color, callback=None, **kwargs):
        super().__init__(parent, width=2*radius, height=2*radius, **kwargs)

        self.radius = radius
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.callback = callback

        # Create the oval (circle) with a border
        self.create_oval(2, 2, 2*radius-2, 2*radius-2, fill=bg_color, outline=border_color, width=0)

        self.create_text(radius, radius, text=text, fill=text_color, font=("Helvetica", 21, "normal"))

        self.bind("<Button-1>", self._on_click)

    def _on_click(self, event):
        if self.callback:
            self.callback()
