import sys
from time import sleep
import time
import tkinter as tk

# Fungsi untuk menampilkan lirik dengan GUI
def display_lyrics_gui():
    # Membuat window
    window = tk.Tk()
    window.title("Lirik Lagu")

    # Mengatur ukuran window (500x300) dan memusatkan posisi window di layar
    window.geometry("500x300")
    window.resizable(False, False)

    # Membuat label untuk menampilkan lirik, dengan teks di tengah
    label = tk.Label(window, text="", font=("Helvetica", 14), anchor="center", justify="center", wraplength=400)
    label.pack(expand=True)

    # Fungsi untuk menampilkan lirik setelah tombol Mulai ditekan
    def start_lyrics():
        # Nonaktifkan tombol setelah ditekan
        start_button.config(state="disabled")

        # Lirik dan delay antar karakter serta antar baris
        lines = [
            ("Cause you are the piece of me", 0.08),
            ("I wish I didn't need", 0.10),
            ("Chasing relentlessly", 0.10),
            ("Still fight and i don't know why", 0.09),
            ("If our love is tragedy", 0.14),
            ("Why are you my remedy?", 0.10),
            ("If our love insanity", 0.11),
            ("Why are you my clarity", 0.09),
            ("••••", 7.60),
            ("If our love is tragedy", 0.14),
            ("Why are you my remedy?", 0.10),
            ("If our love insanity", 0.11),
            ("Why are you my clarity", 0.09),
        ]

        delays = [1.3, 1.8, 1.8, 1.0, 0.7, 1.0, 1.3, 1.3, 0.5, 0.7, 1.0, 1.3, 1.3]

        def show_lyrics(line, char_delay, line_delay, idx):
            if idx >= len(lines):
                return
            text, char_delay = lines[idx]

            # Menampilkan teks karakter demi karakter
            current_text = ""
            for char in text:
                current_text += char
                label.config(text=current_text)
                window.update()
                sleep(char_delay)

            sleep(line_delay)

            window.after(0, lambda: show_lyrics(*lines[idx + 1], delays[idx + 1], idx + 1))

        show_lyrics(*lines[0], delays[0], 0)

    start_button = tk.Button(window, text="Press", font=("Helvetica", 14), command=start_lyrics)
    start_button.pack(pady=10)

    window.mainloop()

display_lyrics_gui()