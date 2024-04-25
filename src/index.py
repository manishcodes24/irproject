# index.py


from collections import defaultdict


class ForwardIndex:
    def __init__(self):
        self.index = {}

    def build_index(self, all_document_tokens, file_dictionary):
        for doc_id, tokens in all_document_tokens.items():
            word_frequency = {}
            for token in tokens:
                if token not in word_frequency:
                    word_frequency[token] = 1
                else:
                    word_frequency[token] += 1
            file_id = file_dictionary.document_to_id[doc_id]
            if file_id not in self.index:
                self.index[file_id] = {}
            self.index[file_id] = word_frequency

    def write_to_file(self, output_file):
        with open(output_file, "w") as f:
            f.write("Forward Index\n")
            f.write("File ID\tWords\n")
            for file_id, word_freq in sorted(self.index.items()):
                words_str = "; ".join(
                    f"{word} ({freq})" for word, freq in sorted(word_freq.items())
                )
                f.write(f"{file_id}\t\t{words_str}\n")


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
            f.write("Word\t\tDocuments\n")
            for word, doc_freqs in sorted(self.index.items()):
                docs_str = "; ".join(
                    f"{doc_name}: {freq}"
                    for doc_name, freq in sorted(doc_freqs.items())
                )
                f.write(f"{word.ljust(15)}\t{docs_str}\n")
