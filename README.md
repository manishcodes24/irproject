# Text Parser Project

This project provides a text parsing functionality to tokenize documents, build word and file dictionaries, and generate dictionary output file.

## How to Run the Code

1. Create a virtual environment in your local machine.
2. Ensure you have Python installed on your system.
3. Install the required dependencies by running: `pip install -r requirements.txt`
4. Run the `main.py` script.
5. The script will prompt you to confirm whether all the data files are in .txt format. Enter 'yes' or 'no'.
6. If you enter 'yes' or 'y', the script will parse the text files and build dictionaries. Once finished, it will generate an output file named `parser_output.txt` in the project folder.
7. If you enter 'no' or 'n', the script will remind you to ensure all files in the specified folder path are in .txt format before proceeding.

## Project Structure

- `main.py`: Main script to run the text parsing functionality.
- `src/`: Contains the source code for the project modules.
  - `stemming/` : Contains Porter.java and stemmer.h(we have used PorterStemmer from NLTK for this project)
  - `tokenizer.py`: Module for tokenizing documents.
  - `text_parser.py`: Module for text parsing.
  - `word_dictionary.py`: Module for building the word dictionary.
  - `file_dictionary.py`: Module for building the file dictionary.
- `data/`: Contains the following:
  - `ft911/`: This folder contains 15 data files in `.txt` format.
  - `stopwordlist.txt`: A file containing a list of stopwords.
- `requirements.txt`: File containing a list of dependencies required to run the project.
- `README.md`: This file, containing information about the project.

## Contact

For any inquiries or issues regarding this project, please contact:
Manish Raghunathareddy
ManishRaghunathareddy@my.unt.edu
