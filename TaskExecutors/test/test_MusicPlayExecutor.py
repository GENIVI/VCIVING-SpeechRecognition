# Note: This is just a test file used to test/debug the TaskExecutors.
# This is not incorporated into EmulationCore by any means.

from MusicPlayExecutor.MusicPlayExecutor import MusicPlayExecutor


def play_song(spoken_sentence):
    music_exec = MusicPlayExecutor()
    music_exec.run([spoken_sentence])


# Different ways of asking to play music
play_song("play Kasun Kalhara's Sanda Mithuri song")
# play
# play Kasun
# play Kasun Kalhara's
# play Kasun Kalhara's Sanda
# play_song("play Sepalika Mala by Jayasiri Amarasekara")

# Dropping certain letters in the song name
# Real song is Pransa Yuwathiya Amal Perera
# play_song("play Pransa Yuwath by Amal Perera")

# Following does not work.
# play_song("play Baby by Justin Bieber")
