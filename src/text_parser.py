import os
from collections import defaultdict
from .tokenizer import Tokenizer
from .word_dictionary import WordDictionary
from .file_dictionary import FileDictionary
from .forward_index import build_forward_index
from .inverted_index import build_inverted_index


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

    def generate_output_file(self):
        output_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "parser_output.txt"
        )  # Store in the parent directory of src folder
        return output_file

    def write_dictionaries_to_file(self, output_file):
        with open(output_file, "w", encoding="utf-8") as output:
            output.write("Word Dictionary:\n")
            max_word_length = max(
                len(word) for word in self.word_dictionary.word_to_id.keys()
            )
            for word, word_id in self.word_dictionary.word_to_id.items():
                output.write(f"{word.ljust(max_word_length)} {word_id}\n")

            output.write("\nFile Dictionary:\n")
            for doc_no, doc_id in self.file_dictionary.document_to_id.items():
                output.write(f"{doc_no}         {doc_id}\n")
