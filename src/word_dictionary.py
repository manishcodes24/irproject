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
