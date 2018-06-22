import googlesearch
import urllib.request

# TODO: To be completed later on.
# Cannot be used to-date
class GoogleForMusic:

    FILE_TYPE = "mp3"
    HTML_FILE_NAME_BEGIN_CHARACTER = "\""
    ABSOLUTE_PATH_STARTERS = ["http://", "ftp://"]

    def _get_file_names_in_url_content(self, url_content):
        file_names = []
        try:
            file_type_first_index = url_content.index(self.FILE_TYPE)
            url_content_upto_first_index = url_content[:file_type_first_index + 1]
            file_name_begin_index = url_content_upto_first_index.rindex(self.HTML_FILE_NAME_BEGIN_CHARACTER) + 1
            # Should stop after gaining fill extension name
            file_name_end_index = file_type_first_index + len(self.FILE_TYPE)
            file_name = url_content[file_name_begin_index:file_name_end_index]
            file_names.append(file_name)

        except Exception:
            return file_names

    def _is_absolute_dir_song_filepath(self, filepath):
        return filepath.startswith(absolute_path_starter for absolute_path_starter in self.ABSOLUTE_PATH_STARTERS)

    def _is_relative_dir_song_filepath(self, filepath):
        return not self._is_absolute_dir_song_filepath(filepath)

    def search(self, song_name):
        search_query = song_name + " " + "mp3"
        search_result = googlesearch.search(search_query, stop=10)
        for url in search_result:
            print("Trying URL: " + url)
            try:
                url_contents = urllib.request.urlopen(url).read().decode("utf-8")
                song_files_in_url_contents = self._get_file_names_in_url_content(url_contents)
                print(song_files_in_url_contents)

            except:
                continue