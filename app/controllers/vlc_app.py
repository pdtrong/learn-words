import vlc
import time


def play_sound_of_word(file_path, delay=1):
    vlc_app = vlc.MediaPlayer(file_path)
    vlc_app.play()
    time.sleep(delay)
