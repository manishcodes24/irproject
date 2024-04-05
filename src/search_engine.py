# search_engine.py

from nltk.stem import PorterStemmer


class SearchEngine:
    def __init__(self, stopword_file, inverted_index):
        self.stopword_file = stopword_file
        self.inverted_index = inverted_index
        self.stemmer = PorterStemmer()

    def is_stopword(self, word):
        with open(self.stopword_file, "r", encoding="utf-8") as stopword_file:
            stopwords = set(line.strip() for line in stopword_file)
        return word.lower() in stopwords

    def stem_word(self, word):
        return self.stemmer.stem(word)

    def search_word(self, word):
        if not self.is_stopword(word):
            stemmed_word = self.stem_word(word)
            if stemmed_word in self.inverted_index.index:
                posting_list = self.inverted_index.index[stemmed_word]
                return f"{word} : {posting_list}"
            else:
                return f'"{word}" is not found in the dictionary.\n'
        else:
            return f'"{word}" is a stopword.\n'
