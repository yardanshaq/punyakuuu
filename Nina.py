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
        ("Ini sumpahku padamu tuk biarkanmu", 0.1),
        ("Tumbuh lebih baik", 0.1),
        ("Cari panggilanmu", 0.1),
        ("Jadi lebih baik", 0.1),
        ("Dibanding diriku", 0.1),
        ("Tuk sementara", 0.1),
        ("Kita", 0.1),
        ("Tertawakan", 0.1),
        ("Berbagai hal", 0.1),
        ("Yang lucu dan lara", 0.1),
        ("Selepas lepasnya", 0.1),
        ("Saat dewasa kau kan mengerti", 0.1),
        ("Karena kelak kau kan tersakiti", 0.1)
    ]
    delays = [0.1, 0.2, 6.0, 8.6, 11.0, 14.0, 16.0, 17.2, 19.0, 21.0, 24.0, 26.6, 32.0]
    
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