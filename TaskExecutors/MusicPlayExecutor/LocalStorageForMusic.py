import os
import operator
from mutagen.easyid3 import EasyID3
from MusicPlayExecutor.Algorithm import Algorithm


# Currently we use the title tag to filter out the song from the storage.
# This is NOT intelligent.
# We intend to to the following procedure in order to make local audio-search intelligent.
# 1. Iterate through each an every audio file inside the music_folderpath directory.
# 2. Open each file and convert its audio to a wave format.
# 3. Use that wave format and remove(distinguish between) the music and the lyrics.
# 4. Grab the lyrics and search for the given title inside the lyrics.
# 5. If lyrics contains the given song name(title), present that as a match to the next level of processing.
# This is to be done after completing most of the functionality of the EmulationCore.
class LocalStorageForMusic:

    METADATA_KEY_TITLE = "title"
    METADATA_KEY_ARTIST = "artist"

    KEY_SONG_TITLE = "song_title"
    KEY_SONG_ARTIST = "song_artist"
    KEY_SONG_SCORE = "song_score"

    def __init__(self, music_folderpath):
        self._music_folderpath = music_folderpath

    # This method is used to confirm the song title is same as the requested song name.
    # Whatever the algorithm that compares the two titles should be implemented here.
    @staticmethod
    def _score_title_same_as_heard_title(real_title, heard_title):
        no_space_real_title = real_title.lower().replace(" ", "")
        no_space_heard_title = heard_title.lower().replace(" ", "")

        return Algorithm.score_simple_exponential_search_alg(no_space_real_title, no_space_heard_title)

    # This method is used to confirm whether the heard artist is same as the real artist in the song.
    # Whatever the algorithm that compares the two artist names should be implemented here.
    @staticmethod
    def _score_artist_same_as_heard_artist(real_artist, heard_artist):
        no_space_real_artist = real_artist.lower().replace(" ", "")
        no_space_heard_artist = heard_artist.lower().replace(" ", "")

        return Algorithm.score_simple_exponential_search_alg(no_space_real_artist, no_space_heard_artist)

    # Returns normalized dictionary which contains values normalized between 0.0 and 1.0 with respect to the given
    # dictionary.
    @staticmethod
    def _get_normalized_info_dict(info_dict):
        min_score_possible = 0.0
        max_score_possible = max(info_dict.items(), key=operator.itemgetter(1))[1]

        for key in info_dict:
            unnorm_score = info_dict[key]
            norm_score = Algorithm.get_normalized_value(unnorm_score, min_score_possible, max_score_possible, 0.0, 1.0)

            info_dict[key] = norm_score

        return info_dict

    def _score_songs_and_titles_in_sentence(self, sentence):
        file_set_to_search = os.listdir(self._music_folderpath)
        splitted_sentence = sentence.split(" ")

        scores_for_songs = {}
        scores_for_assumed_titles = {}
        for file_name in file_set_to_search:
            try:
                file_name = self._music_folderpath + "/" + file_name
                audio_file = EasyID3(file_name)
                audio_file_title = audio_file[LocalStorageForMusic.METADATA_KEY_TITLE][0]
                audio_file_artist = audio_file[LocalStorageForMusic.METADATA_KEY_ARTIST][0]

                # At this point, it is safe to assume the file is an audio format.
                # Therefore we can assign it a place in scores_for_song_titles dictionary.
                score_for_song = {}
                for assumed_title_begin_index in range(len(splitted_sentence)):
                    for assumed_title_end_index in range(assumed_title_begin_index, len(splitted_sentence)):
                        assumed_title = " ".join(splitted_sentence[assumed_title_begin_index:assumed_title_end_index + 1])
                        assumed_title_score = self._score_title_same_as_heard_title(audio_file_title, assumed_title)

                        score_for_song[assumed_title] = assumed_title_score
                        scores_for_assumed_titles[assumed_title] = (scores_for_assumed_titles[assumed_title] if assumed_title in scores_for_assumed_titles else 0.0) + assumed_title_score

                # Normalize the score_for_song dictionary
                score_for_song = self._get_normalized_info_dict(score_for_song)

                score_data_for_song = {
                    self.KEY_SONG_TITLE: audio_file_title,
                    self.KEY_SONG_ARTIST: audio_file_artist,
                    self.KEY_SONG_SCORE: score_for_song
                }
                scores_for_songs[audio_file] = score_data_for_song

            except:
                continue

        # We have to adjust the scores according to the assumed title being a real title by passing it through a certain
        # model. This model should reduce the score for including words which would not preferably exist in song titles.

        return scores_for_songs, self._get_normalized_info_dict(scores_for_assumed_titles)

    def get_title_from_sentence(self, sentence):
        score_songs_for_titles, scores_titles_in_sentence = self._score_songs_and_titles_in_sentence(sentence)
        deduced_title = max(scores_titles_in_sentence.items(), key=operator.itemgetter(1))[0]

        real_title = ""
        real_title_score = 0.0

        for song in score_songs_for_titles:
            song_data_scores = score_songs_for_titles[song]
            song_real_title = song_data_scores[self.KEY_SONG_TITLE]

            song_title_scores = song_data_scores[self.KEY_SONG_SCORE]
            real_title_deduced_score = song_title_scores[deduced_title]

            if real_title_deduced_score > real_title_score:
                real_title = song_real_title
                real_title_score = real_title_deduced_score

        return real_title

    def _score_songs_and_artists_in_sentence(self, sentence):
        file_set_to_search = os.listdir(self._music_folderpath)
        splitted_sentence = sentence.split(" ")

        scores_for_songs = {}
        scores_for_assumed_artists = {}
        for file_name in file_set_to_search:
            try:
                file_name = self._music_folderpath + "/" + file_name
                audio_file = EasyID3(file_name)
                audio_file_title = audio_file[LocalStorageForMusic.METADATA_KEY_TITLE][0]
                audio_file_artist = audio_file[LocalStorageForMusic.METADATA_KEY_ARTIST][0]

                # At this point, it is safe to assume the file is an audio format.
                # Therefore we can assign it a place in scores_for_song_titles dictionary.
                score_for_song = {}
                for assumed_artist_begin_index in range(len(splitted_sentence)):
                    for assumed_artist_end_index in range(assumed_artist_begin_index, len(splitted_sentence)):
                        assumed_artist = " ".join(splitted_sentence[assumed_artist_begin_index:assumed_artist_end_index + 1])
                        assumed_artist_score = self._score_artist_same_as_heard_artist(audio_file_artist, assumed_artist)

                        score_for_song[assumed_artist] = assumed_artist_score
                        scores_for_assumed_artists[assumed_artist] = (scores_for_assumed_artists[assumed_artist] if assumed_artist in scores_for_assumed_artists else 0.0) + assumed_artist_score

                # Normalize the score_for_song dictionary
                score_for_song = self._get_normalized_info_dict(score_for_song)

                score_data_for_song = {
                    self.KEY_SONG_TITLE: audio_file_title,
                    self.KEY_SONG_ARTIST: audio_file_artist,
                    self.KEY_SONG_SCORE: score_for_song
                }
                scores_for_songs[audio_file] = score_data_for_song

            except:
                continue

        return scores_for_songs, self._get_normalized_info_dict(scores_for_assumed_artists)

    def get_artist_from_sentence(self, sentence):
        score_songs_for_artists, score_artists_in_sentence = self._score_songs_and_artists_in_sentence(sentence)
        deduced_artist = max(score_artists_in_sentence.items(), key=operator.itemgetter(1))[0]

        real_artist = ""
        real_artist_score = 0.0

        for song in score_songs_for_artists:
            song_data_scores = score_songs_for_artists[song]
            song_real_artist = song_data_scores[self.KEY_SONG_ARTIST]

            song_artist_scores = song_data_scores[self.KEY_SONG_SCORE]
            real_artist_deduced_score = song_artist_scores[deduced_artist]

            if real_artist_deduced_score > real_artist_score:
                real_artist = song_real_artist
                real_artist_score = real_artist_deduced_score

        return real_artist

    def search(self, sentence):
        song_title = self.get_title_from_sentence(sentence)
        song_artist = self.get_artist_from_sentence(sentence)

        file_set_to_search = os.listdir(self._music_folderpath)
        for file_name in file_set_to_search:
            try:
                file_name = self._music_folderpath + "/" + file_name
                audio_file = EasyID3(file_name)
                audio_file_title = audio_file[LocalStorageForMusic.METADATA_KEY_TITLE][0]
                audio_file_artist = audio_file[LocalStorageForMusic.METADATA_KEY_ARTIST][0]

                if song_title == audio_file_title and song_artist == audio_file_artist:
                    return open(file_name, "rb")

            except:
                continue

        return None
