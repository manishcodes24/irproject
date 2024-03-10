import os
from src.text_parser import TextParser
from src.word_dictionary import WordDictionary
from src.file_dictionary import FileDictionary


def generate_output_file(folder_path, dictionary_type):
    if dictionary_type == "word":
        output_file = os.path.join(folder_path, "word_dictionary.txt")
    elif dictionary_type == "file":
        output_file = os.path.join(folder_path, "file_dictionary.txt")
    else:
        raise ValueError("Invalid dictionary type provided")
    return output_file


def write_dictionaries_to_file(output_file, parser):
    with open(output_file, "w", encoding="utf-8") as output:
        output.write("Word Dictionary:\n")
        max_word_length = max(
            len(word) for word in parser.word_dictionary.word_to_id.keys()
        )
        for word, word_id in parser.word_dictionary.word_to_id.items():
            output.write(f"{word.ljust(max_word_length)} {word_id}\n")

        output.write("\nFile Dictionary:\n")
        for doc_no, doc_id in parser.file_dictionary.document_to_id.items():
            output.write(f"{doc_no}         {doc_id}\n")


def main():
    current_directory = os.path.dirname(__file__)
    folder_path = os.path.abspath(os.path.join(current_directory, "data", "ft911"))
    stopword_file = os.path.abspath(
        os.path.join(current_directory, "data", "stopwordlist.txt")
    )
    output_path = current_directory  # Set output path to the same project folder

    confirmation = input(
        "\nAre all the data files in .txt format? (yes/y or no/n): \n"
    ).lower()
    if confirmation in ["yes", "y"]:
        print("\nParsing text files and building dictionaries...\n")
        parser = TextParser(folder_path, stopword_file)
        all_document_tokens = parser.tokenize_files_in_folder()
        parser.build_dictionaries(all_document_tokens)

        parser_output_file = os.path.join(output_path, "parser_output.txt")
        write_dictionaries_to_file(parser_output_file, parser)

        print("\nParser output file generated:", parser_output_file, "\n")
    elif confirmation in ["no", "n"]:
        print(
            "\nPlease ensure all files in the folder path are in .txt format before running the program.\n"
        )
    else:
        print("\nInvalid input. Please enter 'yes' or 'no'.\n")


if __name__ == "__main__":
    main()
