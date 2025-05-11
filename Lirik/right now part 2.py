import time
from threading import Thread, Lock
import sys

lock = Lock()

# Emoji → RGB Color
COLOR_MAP = {
    "🌸": (255, 105, 180),
    "💎": (0, 255, 255),
    "": (255, 0, 0), 
    "🎄": (0, 128, 0), # hijau
    "🌈": (255, 182, 193), #pink
    "💕": (255, 69, 0), # merah
    "🎈": (231, 76, 60),
    "💡": (255, 191, 0),
    "💛": (255, 255, 0),     # baris ke-2: kuning terang
    "🟢": (0, 255, 128),     # baris ke-6: hijau toska
    "🔵": (128, 128, 255),   # baris ke-8: biru pastel
}


# Konversi RGB ke ANSI escape code
def rgb_to_ansi(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

# Ambil warna dari emoji di akhir lirik
def get_target_color(text):
    for c in reversed(text):
        if c in COLOR_MAP:
            return COLOR_MAP[c]
    return (255, 255, 255)  # Default ke putih

# Animasi teks berwarna
def animate_text(text, delay=0.05, fade_steps=10, fade_delay=0.03):
    with lock:
        text = text.strip('\n')
        target_r, target_g, target_b = get_target_color(text)
        reset_code = "\033[0m"

        fade_progress = []
        typed_chars = []

        for i, char in enumerate(text):
            typed_chars.append(char)
            fade_progress.append(0.0)

            # Update progress setiap huruf yang sudah muncul
            for j in range(len(fade_progress)):
                if fade_progress[j] < 1.0:
                    fade_progress[j] += 1.0 / fade_steps
                    fade_progress[j] = min(fade_progress[j], 1.0)

            # Cetak baris dengan progress sekarang
            line = ""
            for k, c in enumerate(typed_chars):
                prog = fade_progress[k]
                r = int(255 + (target_r - 255) * prog)
                g = int(255 + (target_g - 255) * prog)
                b = int(255 + (target_b - 255) * prog)
                color_code = rgb_to_ansi(r, g, b)
                line += f"{color_code}{c}{reset_code}"

            sys.stdout.write("\r" + line + " " * (len(text) - len(typed_chars)))  # clear sisa
            sys.stdout.flush()
            time.sleep(delay)

        # ✨ Lanjutkan fading untuk sisa huruf yang belum full 1.0
        while any(p < 1.0 for p in fade_progress):
            for j in range(len(fade_progress)):
                if fade_progress[j] < 1.0:
                    fade_progress[j] += 1.0 / fade_steps
                    fade_progress[j] = min(fade_progress[j], 1.0)

            # Redraw with updated colors
            line = ""
            for k, c in enumerate(typed_chars):
                prog = fade_progress[k]
                r = int(255 + (target_r - 255) * prog)
                g = int(255 + (target_g - 255) * prog)
                b = int(255 + (target_b - 255) * prog)
                color_code = rgb_to_ansi(r, g, b)
                line += f"{color_code}{c}{reset_code}"

            sys.stdout.write("\r" + line)
            sys.stdout.flush()
            time.sleep(fade_delay)

        sys.stdout.write("\n")
        sys.stdout.flush()

# Fungsi untuk menyanyikan satu baris lirik
def sing_lyric(lyric, delay, speed):
    time.sleep(delay)
    animate_text(lyric, speed)

# Lirik dan waktu delay
def sing_song():
    lyrics = [
        ("Right now 🌸", 0.11),
        ("I wish you were here with me 💎", 0.07),
        ("Cause right now 💕", 0.09),
        ("Everything is new to me 🎄", 0.09),
        ("You know I can't fight the feeling 🌈", 0.10),
        ("And every night I feel it 💛", 0.09),
        ("Right now 🎈", 0.11),
        ("I wish you were here with me 💡", 0.07),
    ]
    delays = [0.3, 2.2, 7.5, 10.0, 16.2, 20.5, 24.0, 26.0]
    
    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed))
        threads.append(t)
        t.start()
    
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()
#yardanshaq