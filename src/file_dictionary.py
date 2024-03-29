class FileDictionary:
    def __init__(self):
        self.document_to_id = {}
        self.current_document_id = 1

    def build(self, all_document_tokens):
        # Create a list of (doc_no, tokens) tuples sorted by doc_no's numerical value
        sorted_doc_tuples = sorted(
            all_document_tokens.items(), key=lambda x: extract_number(x[0])
        )

        for doc_no, _ in sorted_doc_tuples:
            if doc_no not in self.document_to_id:
                self.document_to_id[doc_no] = self.current_document_id
                self.current_document_id += 1


def extract_number(doc_no):
    # Extract the numerical value from the document ID
    return int(doc_no.split("-")[1])
