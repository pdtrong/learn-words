import os
import glob


def remove_mp3_files(path_root):
    files = glob.glob(path_root + '/' + 'temporary' + '/' + '*.mp3')
    [os.remove(f) for f in files]