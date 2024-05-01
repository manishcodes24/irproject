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

        # Define output file paths for each instance
        output_files = {
            "title": os.path.join(output_path, "output", "1_vsm_output_title.txt"),
            "title_desc": os.path.join(
                output_path, "output", "1_vsm_output_title_desc.txt"
            ),
            "title_narr": os.path.join(
                output_path, "output", "1_vsm_output_title_narr.txt"
            ),
        }

        # Performance Metrics Dictionary
        precision_recall = {}

        # Process each topic
        for topic, query_tf_idf in queries_tf_idf.items():
            precision_recall[topic] = {}
            for instance, output_file in output_files.items():
                # Update the retrieval process based on the instance
                if instance == "title":
                    title_tokens = tokenizer.tokenize_text(query_info[topic]["title"])
                    all_tokens = title_tokens
                elif instance == "title_desc":
                    title_tokens = tokenizer.tokenize_text(query_info[topic]["title"])
                    description_tokens = tokenizer.tokenize_text(
                        query_info[topic].get("description", "")
                    )
                    all_tokens = title_tokens + description_tokens
                elif instance == "title_narr":
                    title_tokens = tokenizer.tokenize_text(query_info[topic]["title"])
                    narrative_tokens = tokenizer.tokenize_text(
                        query_info[topic].get("narrative", "")
                    )
                    all_tokens = title_tokens + narrative_tokens

                # Calculate TF*IDF weights for each query term
                query_tf_idf = {}
                for token in set(all_tokens):
                    tf_title = title_tokens.count(token)
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

                    query_tf_idf[token] = {"tf_idf_title": tf_idf_title}

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
                    with open(output_file, "a") as f:
                        f.write(f"{topic}\t\t{doc_name}\t\t{i}\t\t{relevance_score}\n")

                # Calculate precision and recall
                retrieved_docs = [doc[0] for doc in ranked_docs]
                relevant_docs_for_topic = (
                    parse_qrels_file(qrels_file).get(topic, {}).keys()
                )
                precision, recall = calculate_precision_recall(
                    retrieved_docs, relevant_docs_for_topic
                )
                precision_recall[topic][instance] = {
                    "precision": precision,
                    "recall": recall,
                }

        # Print Performance Metrics in Table Format
        print("\nPerformance Metrics:\n")
        print("{:<10} {:<15} {:<15}".format("Topic", "Precision", "Recall"))
        for topic, info in precision_recall.items():
            precision_title = info["title"]["precision"]
            recall_title = info["title"]["recall"]
            precision_desc = info["title_desc"]["precision"]
            recall_desc = info["title_desc"]["recall"]
            precision_narr = info["title_narr"]["precision"]
            recall_narr = info["title_narr"]["recall"]

            print("{:<10} {:<15} {:<15}".format(topic, "Title", ""))
            print("{:<10} {:<15} {:<15}".format("", precision_title, recall_title))
            print("{:<10} {:<15} {:<15}".format("", "", ""))  # Blank line

            print("{:<10} {:<15} {:<15}".format("", "Title + Description", ""))
            print("{:<10} {:<15} {:<15}".format("", precision_desc, recall_desc))
            print("{:<10} {:<15} {:<15}".format("", "", ""))  # Blank line

            print("{:<10} {:<15} {:<15}".format("", "Title + Narrative", ""))
            print("{:<10} {:<15} {:<15}".format("", precision_narr, recall_narr))
            print("{:<10} {:<15} {:<15}".format("", "", ""))  # Blank line

    elif confirmation in ["no", "n"]:
        print(
            "\nPlease ensure all files in the folder path are in .txt format before running the program.\n"
        )
    else:
        print("\nInvalid input. Please enter 'yes' or 'no'.\n")


if __name__ == "__main__":
    main()
