# inverted_index.py

from collections import defaultdict


class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(dict)

    def build_index(self, all_document_tokens, file_dictionary):
        for doc_name, tokens in all_document_tokens.items():
            for token in set(tokens):
                if token not in self.index:
                    self.index[token] = {}
                self.index[token][doc_name] = tokens.count(token)

    def write_to_file(self, output_file):
        with open(output_file, "w") as f:
            f.write("Inverted Index\n")
            f.write("Word\t\tDocuments\n")  # Adjusted spacing here
            for word, doc_freqs in sorted(self.index.items()):
                docs_str = "; ".join(
                    f"{doc_name}: {freq}"
                    for doc_name, freq in sorted(doc_freqs.items())
                )
                f.write(f"{word.ljust(15)}\t{docs_str}\n")  # Adjusted spacing here


def build_inverted_index(all_document_tokens, file_dictionary):
    inverted_index = InvertedIndex()
    inverted_index.build_index(all_document_tokens, file_dictionary)
    return inverted_index
