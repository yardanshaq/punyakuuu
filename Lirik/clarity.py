import time
from threading import Thread, Lock
import sys

lock = Lock()

def animate_text(text, delay=0.1):
    with lock:
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

def sing_lyric(lyric, delay, speed):
    time.sleep(delay)
    animate_text(lyric, speed)

def sing_song():
    lyrics = [
        ("Cause you are the piece of me", 0.08), 
        ("I wish I didn't need", 0.10),
        ("Chasing relentlessly", 0.10),
        ("Still fight and i don't now why", 0.09),
        ("If our love is tragedy", 0.14),
        ("Why are you my remedy?", 0.10),
        ("If our love insanity", 0.11),
        ("Why are you my clarity?", 0.09),
        ("....", 7.75),
        ("If our love is tragedy", 0.14),
        ("Why are you my remedy?", 0.10),
        ("If our love insanity", 0.11),
        ("Why are you my clarity?", 0.09),

    ]
    
    delays = [0.3, 4.1, 7.9, 11.5, 15.5, 19.2, 23.3, 26.9, 27.2, 57.0, 64.5, 67.8, 72.2]

    
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