import gdown
import threading
import time
from tkinter import Tk, Label, StringVar
from playsound import playsound

# Download MP3
gdown.download("https://drive.google.com/uc?id=1zijS4WNfnGpAsGvAa0nD0V0OUM3dR1hZ", "dj_tante.mp3", quiet=True)

# (text, target_time, speed, color)
# Lyrics data
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

# GUI setup
root = Tk()
root.title("🎶 DJ Sudah Terbiasa Terjadi Tante 🎶")
root.geometry("900x300")
root.configure(bg="black")

lyric_var = StringVar()
label = Label(root, textvariable=lyric_var, font=("Helvetica", 24, "bold"),
            fg="magenta", bg="black", wraplength=750, justify="center")
label.pack(expand=True)

# Event for synchronization
# between audio and lyrics
start_event = threading.Event()

# Main stopwatch + animation loop
def run_lyrics():
    start_event.wait()
    start_time = time.time()
    shown = [False] * len(lyrics)

    def loop():
        now = time.time() - start_time
        for i, (text, target_time, speed, color) in enumerate(lyrics):
            if not shown[i] and now >= target_time:
                shown[i] = True
                label.config(fg=color)  # Change color
                animate_text(text, speed)
        if any(not s for s in shown):
            root.after(30, loop)

    loop()


# Show text with animation
def animate_text(text, speed):
    def inner(idx=1):
        if idx <= len(text):
            lyric_var.set(text[:idx])
            label.update() # Update the label
            root.after(speed, inner, idx + 1)
    inner()



# Play music trigger start_event
def play_audio():
    time.sleep(0.3)  # little delay to ensure the GUI is ready
    start_event.set()
    playsound("dj_tante.mp3")

# Start
threading.Thread(target=play_audio, daemon=True).start()
threading.Thread(target=run_lyrics, daemon=True).start()
root.mainloop()
# yardanshaq