import re
from nltk.stem import PorterStemmer
from collections import defaultdict


class Tokenizer:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def tokenize_text(self, text):
        tokens = re.findall(r"\b(?:[^\W\d_]+(?:[^\W\d_]+[^\W\d_]*)*)\b", text.lower())
        stemmed_tokens = [self.stemmer.stem(token) for token in tokens]
        return [token for token in stemmed_tokens if token]

    def remove_stopwords(self, tokens, stopword_file):
        with open(stopword_file, "r", encoding="utf-8") as stopword_file:
            stopwords = set(line.strip() for line in stopword_file)
        return [token for token in tokens if token.lower() not in stopwords]

    def tokenize_file(self, file_path, stopword_file):
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
        doc_matches = re.finditer(r"<DOCNO>(.*?)</DOCNO>", text)
        text_matches = re.finditer(r"<TEXT>(.*?)</TEXT>", text, re.DOTALL)
        document_tokens = defaultdict(list)
        for doc_match, text_match in zip(doc_matches, text_matches):
            doc_no = doc_match.group(1).strip()
            text_content = text_match.group(1)
            tokens = self.tokenize_text(text_content)
            tokens = self.remove_stopwords(tokens, stopword_file)
            document_tokens[doc_no] = tokens
        return document_tokens
