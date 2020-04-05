import vlc
import time


def media_player(file_path, delay=1):
    vlc_app = vlc.MediaPlayer(file_path)
    vlc_app.play()
    time.sleep(delay)
