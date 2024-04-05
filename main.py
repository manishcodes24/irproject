from src.inverted_index import build_inverted_index
from src.text_parser import TextParser
from src.forward_index import build_forward_index
from src.search_engine import SearchEngine
import os
import time


def main():
    current_directory = os.path.dirname(__file__)
    folder_path = input(
        "\nEnter the path to the folder containing the sample data: \n"
    ).strip()
    stopword_file = os.path.abspath(
        os.path.join(current_directory, "data", "stopwordlist.txt")
    )
    output_path = current_directory  # Set output path to the same folder as main.py

    confirmation = input(
        "\nAre all the data files in .txt format? (yes/y or no/n): \n"
    ).lower()
    if confirmation in ["yes", "y"]:
        print("\nParsing text files and building dictionaries...\n")

        start_time = time.time()  # Record start time

        parser = TextParser(folder_path, stopword_file)
        all_document_tokens = parser.tokenize_files_in_folder()
        parser.build_dictionaries(all_document_tokens)

        # parser_output_file = parser.generate_output_file()
        # parser.write_dictionaries_to_file(parser_output_file)

        # print("Parser output file generated:", parser_output_file)

        forward_index = build_forward_index(all_document_tokens, parser.file_dictionary)
        forward_index_file = os.path.join(output_path, "forward_index.txt")
        forward_index.write_to_file(forward_index_file)
        print("Forward index file generated:", forward_index_file)

        inverted_index = build_inverted_index(
            all_document_tokens, parser.file_dictionary
        )
        inverted_index_file = os.path.join(output_path, "inverted_index.txt")
        inverted_index.write_to_file(inverted_index_file)
        print("Inverted index file generated:", inverted_index_file, "\n")

        end_time = time.time()  # Record end time
        indexing_time = end_time - start_time
        print("Time taken to index the data: {:.2f} seconds".format(indexing_time))

        # Initialize the SearchEngine with the inverted index
        search_engine = SearchEngine(stopword_file, inverted_index)

        # Perform word search
        word_to_search = input("\nEnter the word to search: \n").strip()
        search_result = search_engine.search_word(word_to_search)
        print("\nSearch Result:")
        print(search_result)

    elif confirmation in ["no", "n"]:
        print(
            "\nPlease ensure all files in the folder path are in .txt format before running the program.\n"
        )
    else:
        print("\nInvalid input. Please enter 'yes' or 'no'.\n")


if __name__ == "__main__":
    main()
