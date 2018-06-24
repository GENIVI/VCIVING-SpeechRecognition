from emucorebrain.data.abstracts.TaskExecutor import TaskExecutor
import nltk
from nltk.tag import StanfordNERTagger


class FindMapsExecutor(TaskExecutor):
    # Absolute paths of the Classifier and Stanford NER JAR File
    NER_CLASSIFIER_PATH = "D:/GENIVI/Projects/TaskExecutors/dependencies/entity_recognition/classifiers/english.muc.7class.distsim.crf.ser.gz"
    NER_JAR_PATH = "D:/GENIVI/Projects/TaskExecutors/dependencies/entity_recognition/stanford-ner.jar"

    TAG_ORGANIZATION = "ORGANIZATION"
    TAG_LOCATION = "LOCATION"

    def __init__(self):
        self._tagger = StanfordNERTagger(self.NER_CLASSIFIER_PATH, self.NER_JAR_PATH)

    # Tags the tokens in a given sentence using Stanford NER.
    def _get_tagged_sentence(self, sentence):
        tokenizer = nltk.word_tokenize(sentence)
        return self._tagger.tag(tokenizer)

    # Returns the locations in the given sentence.
    # This method is for usage in the future where one sentence could contain more than one location.
    # For now, we just use the first location returned.
    def _get_locations_from_tags(self, sentence):
        locations = []
        tags = self._get_tagged_sentence(sentence)
        for tag in tags:
            if tag[1] == self.TAG_ORGANIZATION or tag[1] == self.TAG_LOCATION:
                locations.append(tag[0])

        return locations

    # Executes the FindMapsExecutor.
    # The main method executed when prediction is directed to this class.
    def run(self, args):
        data = args[0]
        locations = self._get_locations_from_tags(data)
        print("FindMapsExecutor; Place: " + locations[0])
