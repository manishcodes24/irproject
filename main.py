# main.py

import os
from src.tokenizer import Tokenizer
from src.Utils import parse_topics_file
from src.Utils import parse_qrels_file
from src.Utils import calculate_precision_recall
from src.text_parser import TextParser
from src.index import ForwardIndex
from src.index import InvertedIndex
from src.search import SearchEngine


def main():
    current_directory = os.path.dirname(__file__)
    stopword_file = os.path.abspath(
        os.path.join(current_directory, "data", "stopwordlist.txt")
    )

    output_path = current_directory
    output_directory = os.path.join(output_path, "output")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    folder_path = os.path.abspath(os.path.join(current_directory, "data", "ft911"))
    qrels_file = os.path.abspath(os.path.join(current_directory, "data", "main.qrels"))

    confirmation = input(
        "\nAre all the data files in .txt format? (yes/y or no/n): \n"
    ).lower()
    if confirmation in ["yes", "y"]:
        print("\nParsing text files and building dictionaries...\n")

        # Parse topics file
        topics_file = os.path.abspath(
            os.path.join(current_directory, "data", "topics.txt")
        )
        query_info = parse_topics_file(topics_file)

        # Tokenize queries and calculate TF*IDF weights
        tokenizer = Tokenizer()
        queries_tf_idf = {}
        for topic, info in query_info.items():
            title_tokens = tokenizer.tokenize_text(info["title"])
            description_tokens = tokenizer.tokenize_text(info.get("description", ""))
            narrative_tokens = tokenizer.tokenize_text(info.get("narrative", ""))

            all_tokens = title_tokens + description_tokens + narrative_tokens
            tokens_set = set(all_tokens)
            query_tf_idf = {}
            for token in tokens_set:
                tf_title = title_tokens.count(token)
                tf_description = description_tokens.count(token)
                tf_narrative = narrative_tokens.count(token)
                idf = len(query_info) / (
                    1
                    + sum(
                        1
                        for info in query_info.values()
                        if token in info["title"]
                        or token in info["description"]
                        or token in info["narrative"]
                    )
                )

                tf_idf_title = tf_title * idf
                tf_idf_description = tf_description * idf
                tf_idf_narrative = tf_narrative * idf

                query_tf_idf[token] = {
                    "tf_idf_title": tf_idf_title,
                    "tf_idf_description": tf_idf_description,
                    "tf_idf_narrative": tf_idf_narrative,
                }

            queries_tf_idf[topic] = query_tf_idf

        parser = TextParser(folder_path, stopword_file)
        all_document_tokens = parser.tokenize_files_in_folder()
        parser.build_dictionaries(all_document_tokens)

        parser_output_file = parser.generate_parser_output_file()
        parser.write_parser_output_to_file(parser_output_file)

        forward_index = ForwardIndex()
        forward_index.build_index(all_document_tokens, parser.file_dictionary)
        forward_index_file = os.path.join(output_path, "output", "3_forward_index.txt")
        forward_index.write_to_file(forward_index_file)

        inverted_index = InvertedIndex()
        inverted_index.build_index(all_document_tokens, parser.file_dictionary)
        inverted_index_file = os.path.join(
            output_path, "output", "2_inverted_index.txt"
        )
        inverted_index.write_to_file(inverted_index_file)

        # Calculate total number of documents
        total_docs = len(parser.file_dictionary.document_to_id)

        # Create a search engine instance
        search_engine = SearchEngine(
            stopword_file, inverted_index, parser.file_dictionary, total_docs
        )

        search_engine_output_file = parser.generate_search_engine_output_file()

        # Open the output file for writing
        with open(search_engine_output_file, "w") as f:
            # Process each topic
            for topic, query_tf_idf in queries_tf_idf.items():
                # Retrieve relevant documents and rank them
                relevant_docs = {}
                for term, weights in query_tf_idf.items():
                    posting_list = search_engine.search_term(term)
                    if isinstance(posting_list, dict):
                        for doc_name, term_freq in posting_list.items():
                            doc_id = parser.file_dictionary.document_to_id[doc_name]
                            tf_idf = search_engine.calculate_tf_idf(
                                term_freq, term, doc_id
                            )
                            if doc_name not in relevant_docs:
                                relevant_docs[doc_name] = 0
                            relevant_docs[doc_name] += weights["tf_idf_title"] * tf_idf

                # Sort documents by relevance
                ranked_docs = sorted(
                    relevant_docs.items(), key=lambda x: x[1], reverse=True
                )

                # Write the top relevant documents to the output file
                for i, (doc_name, relevance_score) in enumerate(ranked_docs, 1):
                    f.write(f"{topic}\t\t{doc_name}\t\t{i}\t\t{relevance_score}\n")

                # Calculate precision and recall
                retrieved_docs = [doc[0] for doc in ranked_docs]
                relevant_docs_for_topic = (
                    parse_qrels_file(qrels_file).get(topic, {}).keys()
                )
                precision, recall = calculate_precision_recall(
                    retrieved_docs, relevant_docs_for_topic
                )
                print(f"Topic {topic}: Precision - {precision}, Recall - {recall}")

        print(
            "\nOutput files generated:\nVSM output:",
            search_engine_output_file,
            "\nInverted index:",
            inverted_index_file,
            "\nForward index:",
            forward_index_file,
            "\nParser output:",
            parser_output_file,
        )

    elif confirmation in ["no", "n"]:
        print(
            "\nPlease ensure all files in the folder path are in .txt format before running the program.\n"
        )
    else:
        print("\nInvalid input. Please enter 'yes' or 'no'.\n")


if __name__ == "__main__":
    main()
