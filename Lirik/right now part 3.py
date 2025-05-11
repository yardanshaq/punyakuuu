import pygame
import time
import threading
import re

# Emoji → RGB Color
COLOR_MAP = {
    "🌸": (255, 105, 180),
    "💎": (0, 255, 255),
    "": (255, 0, 0),
    "🎄": (0, 128, 0),
    "🌈": (255, 182, 193),
    "💕": (255, 69, 0),
    "🎈": (231, 76, 60),
    "💡": (255, 191, 0),
    "💛": (255, 255, 0),
    "🟢": (0, 255, 128),
    "🔵": (128, 128, 255),
}

# Ambil warna dari emoji
def get_target_color(text):
    for c in reversed(text):
        if c in COLOR_MAP:
            return COLOR_MAP[c]
    return (255, 255, 255)

# Hapus emoji dari teks (tidak semua font support)
def strip_emojis(text):
    emoji_pattern = re.compile("[\U00010000-\U0010FFFF]", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)

# Setup pygame
pygame.init()
screen = pygame.display.set_mode((700, 300))
pygame.display.set_caption("Lirik")
font = pygame.font.SysFont("Arial", 48)
clock = pygame.time.Clock()
lock = threading.Lock()

def animate_text(text, delay=0.05, fade_steps=10, fade_delay=0.03):
    with lock:
        target_r, target_g, target_b = get_target_color(text)
        text = strip_emojis(text)  # Hapus emoji
        typed_chars = []
        fade_progress = []

        for i, char in enumerate(text):
            typed_chars.append(char)
            fade_progress.append(0.0)

            for j in range(len(fade_progress)):
                if fade_progress[j] < 1.0:
                    fade_progress[j] += 1.0 / fade_steps
                    fade_progress[j] = min(fade_progress[j], 1.0)

            screen.fill((0, 0, 0))
            rendered_text = []
            total_width = 0
            for k, c in enumerate(typed_chars):
                prog = fade_progress[k]
                r = int(255 + (target_r - 255) * prog)
                g = int(255 + (target_g - 255) * prog)
                b = int(255 + (target_b - 255) * prog)
                s = font.render(c, True, (r, g, b))
                rendered_text.append(s)
                total_width += s.get_width()

            x = (screen.get_width() - total_width) // 2
            y = (screen.get_height() - font.get_height()) // 2
            for surf in rendered_text:
                screen.blit(surf, (x, y))
                x += surf.get_width()

            pygame.display.flip()
            time.sleep(delay)

        while any(p < 1.0 for p in fade_progress):
            for j in range(len(fade_progress)):
                if fade_progress[j] < 1.0:
                    fade_progress[j] += 1.0 / fade_steps
                    fade_progress[j] = min(fade_progress[j], 1.0)

            screen.fill((0, 0, 0))
            rendered_text = []
            total_width = 0
            for k, c in enumerate(typed_chars):
                prog = fade_progress[k]
                r = int(255 + (target_r - 255) * prog)
                g = int(255 + (target_g - 255) * prog)
                b = int(255 + (target_b - 255) * prog)
                s = font.render(c, True, (r, g, b))
                rendered_text.append(s)
                total_width += s.get_width()

            x = (screen.get_width() - total_width) // 2
            y = (screen.get_height() - font.get_height()) // 2
            for surf in rendered_text:
                screen.blit(surf, (x, y))
                x += surf.get_width()

            pygame.display.flip()
            time.sleep(fade_delay)

def sing_lyric(lyric, delay, speed):
    time.sleep(delay)
    animate_text(lyric, speed)

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
        t = threading.Thread(target=sing_lyric, args=(lyric, delays[i], speed))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

# Main
sing_song()

# Delay sebentar sebelum keluar
time.sleep(1)
pygame.quit()