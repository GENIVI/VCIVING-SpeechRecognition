# Note: This is just a test file used to test/debug the TaskExecutors.
# This is not incorporated into EmulationCore by any means.

# from Package.Namespace import Class
from MusicPlayExecutor.MusicPlayExecutor import MusicPlayExecutor
from MusicPlayExecutor.GoogleForMusic import GoogleForMusic


def play_song(spoken_sentence):
    music_exec = MusicPlayExecutor()
    music_exec.run([spoken_sentence])


def web_search(song_name : str):
    googler = GoogleForMusic()
    googler.search(song_name)


# web_search("shape of you")
play_song("play Sanda Mithuri song by artist Kasun Kalhara")
# play_song("play Sepalika Mala by Jayasiri Amarasekara")
# play_song("play Pransa Yuwath by Amal Perera")
