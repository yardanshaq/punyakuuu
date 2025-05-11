import gdown
import threading
import time
import math
import random
from tkinter import Tk, Canvas
from playsound import playsound

# Download audio
gdown.download("https://drive.google.com/uc?id=1zijS4WNfnGpAsGvAa0nD0V0OUM3dR1hZ", "dj_tante.mp3", quiet=True)

# Lyrics: (text, time, speed, base color)
lyrics = [
    ("\nsudah terbiasa terjadi tante", 3.3, 80, "cyan"),
    ("teman datang ketika lagi butuh saja", 7.4, 85, "lime"),
    ("coba kalo lagi susah", 11.3, 85, "yellow"),
    ("mereka semua menghilang...", 14.2, 80, "orange"),
    ("apakah spek standar seperti ini yang para pemirsa inginkan?", 17.0, 40, "white"),
    ("tante...", 20.2, 60, "red"),
    ("tante...", 24.1, 60, "hot pink"),
    ("tante...", 27.3, 60, "magenta"),
]

# Setup window
root = Tk()
root.title("🎶 DJ Sudah Terbiasa Terjadi Tante 🎶")
root.geometry("1000x400")
root.configure(bg="black")

canvas = Canvas(root, bg="black", highlightthickness=0)
canvas.pack(fill="both", expand=True)

start_event = threading.Event()
neon_colors = ["cyan", "lime", "magenta", "yellow", "hot pink", "orange", "red"]

# Simpan objek teks agar bisa dihapus
current_chars = []

# Background animasi (lingkaran neon)
circles = []
for _ in range(10):
    x = random.randint(0, 1000)
    y = random.randint(0, 400)
    r = random.randint(40, 100)
    c = random.choice(neon_colors)
    circle = canvas.create_oval(x-r, y-r, x+r, y+r, outline=c, width=1)
    circles.append((circle, x, y, r, c))

def animate_background():
    angle = 0
    while True:
        for i, (circle, x, y, r, c) in enumerate(circles):
            offset = math.sin(angle + i) * 5
            canvas.coords(circle, x-r+offset, y-r+offset, x+r+offset, y+r+offset)
        angle += 0.1
        time.sleep(0.05)

# Tampilkan teks per huruf, dengan efek gelombang dan glow
def animate_text(text, speed, base_color):
    global current_chars
    for item in current_chars:
        canvas.delete(item)
    current_chars = []

    canvas_width = canvas.winfo_width()
    margin = 80
    max_width = canvas_width - margin * 2  # area teks yang tersisa

    n_chars = len(text)
    if n_chars == 0: return  # jika teks kosong

    # Jarak antar huruf otomatis
    x_gap = max(min(25, max_width // n_chars), 12)  # Minimum 12px supaya nggak terlalu rapat

    x_start = margin
    y_base = 180

    def show_letter(i):
        if i >= len(text): return
        char = text[i]
        x = x_start + i * x_gap
        y = y_base + int(10 * math.sin(i))  # efek gelombang naik-turun
        item = canvas.create_text(x, y, text=char,
                                  font=("Comic Sans MS", 32, "bold"),
                                  fill=base_color)
        current_chars.append(item)
        canvas.update()
        root.after(speed, show_letter, i + 1)

    show_letter(0)

    # Efek neon berganti warna
    def glow_loop():
        while any(canvas.type(c) == 'text' for c in current_chars):
            for glow in neon_colors:
                for item in current_chars:
                    canvas.itemconfig(item, fill=glow)
                time.sleep(0.15)
    threading.Thread(target=glow_loop, daemon=True).start()


# Main lyric runner
def run_lyrics():
    start_event.wait()
    start_time = time.time()
    shown = [False] * len(lyrics)

    def loop():
        now = time.time() - start_time
        for i, (text, target_time, speed, color) in enumerate(lyrics):
            if not shown[i] and now >= target_time:
                shown[i] = True
                animate_text(text, speed, color)
        if any(not s for s in shown):
            root.after(30, loop)
    loop()

# Play audio
def play_audio():
    time.sleep(0.5)
    start_event.set()
    playsound("dj_tante.mp3")

# Start threads
threading.Thread(target=play_audio, daemon=True).start()
threading.Thread(target=run_lyrics, daemon=True).start()
threading.Thread(target=animate_background, daemon=True).start()
root.mainloop()
