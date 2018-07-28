

class LocationPreProcessor:

    def __init__(self, locations : list):
        self._locations : list = locations

    def _stem_locations(self):
        self._locations = [location.lower() for location in self._locations]

    def pre_process(self):
        self._stem_locations()

    def get_locations(self):
        return self._locations


class Chunker:

    def __init__(self, to_chunk : str, deep_chunking=True):
        self._to_chunk : str = to_chunk

        self._chunks = []
        for i in range(len(to_chunk)):
            if deep_chunking:
                for j in range(i + 1, len(to_chunk)):
                    self._chunks.append(to_chunk[i:j])
            else:
                self._chunks.append(to_chunk[0:(i + 1)])

    def get_chunked(self):
        return self._chunks
