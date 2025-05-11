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
        ("\nThe apartment we won't share", 0.11),
        ("I wonder what sad wife lives there", 0.11),
        ("Have the windows deciphered her stares?", 0.10),
        ("Do the bricks in the walls know to hide the affairs?", 0.10),
        ("The dog we won't have is now one I would no choose ", 0.09),
        ("The daughter we won't raise still waits for you", 0.09),
        ("The girl I won't be is the one that's yours ", 0.11),
        ("I hope you shortly find what you long for", 0.11),
    ]
    delays = [0.3, 4.9, 10.4, 14.8, 20.8, 26.2, 31.5, 36.8]
    
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