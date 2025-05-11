import gdown
import threading
import time
from tkinter import Tk, Label, StringVar
from playsound import playsound

# Download MP3
gdown.download("https://drive.google.com/uc?id=1WVC1rpB3rido48ZAlEyyjcVnbvDw3IFI", "say_it.mp3", quiet=True)

# (text, target_time, speed, color)
# Lyrics data
lyrics = [
    ("mmm...", 0.3, 80, "magenta"),
    ("when u say like that oh, oh, oh, oh", 2.8, 60, "cyan"),
    ("when u say it, say it", 7.4, 65, "red"),
    ("got me falling right back oh, oh, oh, oh", 9.0, 60, "yellow"),
    ("let me fuck u right back", 14.0, 60, "orange"),
    ("when u say like that oh, oh, oh, oh", 15.5, 60, "cyan"),
    ("when u say it, say it", 20.2, 60, "red"),
    ("let me fuck you right back oh, oh, oh, oh", 22.0, 50, "orange"),
    ("mmm...", 26.5, 80, "magenta"),
]

# GUI setup
root = Tk()
root.title("🎶 Say it - Illenium Remix 🎶")
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
    playsound("say_it.mp3")

# Start
threading.Thread(target=play_audio, daemon=True).start()
threading.Thread(target=run_lyrics, daemon=True).start()
root.mainloop()
# yardanshaq