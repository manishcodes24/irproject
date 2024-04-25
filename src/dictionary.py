# dictionary.py

from .Utils import extract_number




class WordDictionary:
    def __init__(self):
        self.word_to_id = {}
        self.current_word_id = 1

    def build(self, all_document_tokens):
        all_tokens = [
            token for tokens in all_document_tokens.values() for token in tokens
        ]
        sorted_unique_words = sorted(set(all_tokens))
        for word in sorted_unique_words:
            if word not in self.word_to_id:
                self.word_to_id[word] = self.current_word_id
                self.current_word_id += 1


class FileDictionary:
    def __init__(self):
        self.document_to_id = {}
        self.current_document_id = 1

    def build(self, all_document_tokens):
        sorted_doc_tuples = sorted(
            all_document_tokens.items(), key=lambda x: extract_number(x[0])
        )
        for doc_no, _ in sorted_doc_tuples:
            if doc_no not in self.document_to_id:
                self.document_to_id[doc_no] = self.current_document_id
                self.current_document_id += 1
