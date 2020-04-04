import vlc
import time


def play_sound_of_word(file_path):
    p = vlc.MediaPlayer(file_path)
    p.play()
    time.sleep(1)
