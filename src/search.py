# search.py

import math
from nltk.stem import PorterStemmer


class SearchEngine:
    def __init__(self, stopword_file, inverted_index, file_dictionary, total_docs):
        self.stopword_file = stopword_file
        self.inverted_index = inverted_index
        self.file_dictionary = file_dictionary
        self.total_docs = total_docs
        self.stemmer = PorterStemmer()

    def is_stopword(self, word):
        with open(self.stopword_file, "r", encoding="utf-8") as stopword_file:
            stopwords = set(line.strip() for line in stopword_file)
        return word.lower() in stopwords

    def stem_word(self, word):
        return self.stemmer.stem(word)

    def calculate_tf_idf(self, term_freq, term, doc_id):
        tf = term_freq / sum(self.inverted_index.index[term].values())
        idf = math.log(self.total_docs / len(self.inverted_index.index[term]))
        return tf * idf

    def search_term(self, term):
        if not self.is_stopword(term):
            stemmed_term = self.stem_word(term)
            if stemmed_term in self.inverted_index.index:
                posting_list = self.inverted_index.index[stemmed_term]
                return posting_list  # Return posting list for further processing
            else:
                return {}  # Return an empty dictionary if word is not found in index
        else:
            return {}  # Return an empty dictionary if word is a stopword
