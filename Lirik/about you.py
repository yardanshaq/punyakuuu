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
        ("\nDo you think I have forgotten?", 0.1),
        ("Do you think I have forgotten?", 0.1),
        ("Do you think I have forgotten", 0.1),
        ("about you?", 0.2),
        ("There was something bout you that now I cant remember", 0.08),
        ("Its the same damn thing that made my heart surrender", 0.1),
        ("And I miss you on a train, I miss you in the morning", 0.1),
        ("I never know what to think about", 0.1),
        ("I think about youuuuuuuuuuuuuuuuuuuuuuuuuuu", 0.1)
    ]
    delays = [0.3, 5.0, 10.0, 15.0, 20.3, 25.0, 27.0, 30.2, 33.3]

    colors = [Fore.YELLOW, Fore.CYAN, Fore.MAGENTA, Fore.RED, Fore.GREEN, Fore.BLUE, Fore.WHITE, Fore.LIGHTBLACK_EX, Fore.LIGHTWHITE_EX]
    
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