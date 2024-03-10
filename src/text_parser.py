import os
import re
from nltk.stem import PorterStemmer
from collections import defaultdict
from .tokenizer import Tokenizer
from .word_dictionary import WordDictionary
from .file_dictionary import FileDictionary


class TextParser:
    def __init__(self, folder_path, stopword_file):
        self.folder_path = folder_path
        self.stopword_file = stopword_file
        self.tokenizer = Tokenizer()
        self.word_dictionary = WordDictionary()
        self.file_dictionary = FileDictionary()

    def tokenize_files_in_folder(self):
        all_document_tokens = defaultdict(list)
        file_names = sorted(os.listdir(self.folder_path))
        for file_name in file_names:
            if file_name.endswith(".txt"):
                file_path = os.path.join(self.folder_path, file_name)
                document_tokens = self.tokenizer.tokenize_file(
                    file_path, self.stopword_file
                )
                all_document_tokens.update(document_tokens)
        return all_document_tokens

    def build_dictionaries(self, all_document_tokens):
        self.word_dictionary.build(all_document_tokens)
        self.file_dictionary.build(all_document_tokens)
