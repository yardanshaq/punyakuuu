import time
from threading import Thread, Lock
import sys
from colorama import init, Fore, Style

init(autoreset=True)

lock = Lock()

def animate_text(text, delay=0.1, color=Fore.WHITE):
    with lock:
        for char in text:
            sys.stdout.write(color + char)
            sys.stdout.flush()
            time.sleep(delay)
        print(Style.RESET_ALL)


def sing_lyric(lyric, delay, speed, color):
    time.sleep(delay)
    animate_text(lyric, speed, color)

def sing_song():
    lyrics = [
        ("\nIf you dance, I'll dance", 0.09),
        ("I'll put my red dress on, get it on", 0.09),
        ("And if you fight, I'll fight", 0.09),
        ("It doesn't matter now, it's all gone", 0.09),
        ("\nI've got my mind on you", 0.10),
        ("I got my mind on you", 0.09),
    ]
    delays = [0.3, 4.6, 9.5, 14.0, 18.2, 23.5]

    colors = [Fore.CYAN, Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.BLUE, Fore.MAGENTA]

    threads = []
    for i in range(len(lyrics)):
        lyric, speed = lyrics[i]
        t = Thread(target=sing_lyric, args=(lyric, delays[i], speed, colors[i % len(colors)]))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    sing_song()
#yardanshaq