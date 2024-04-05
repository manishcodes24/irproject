# Text Parser Project

This project provides functionality for text parsing, including tokenization of documents, building word and file dictionaries, and generating dictionary output files. Additionally, it includes a search engine module for searching terms in the built indexes.

## How to Run the Code

1. Ensure you have Python installed on your system.
2. Create a virtual environment in your local machine.
   `python -m venv venv`
   Activate virtual environment
   `source venv/bin/activate` # On Linux/Mac
   `venv\Scripts\activate` # On Windows
3. Install the required dependencies by running: `pip install -r requirements.txt`
4. Run the `main.py` script.
5. Enter 'trec' to process TREC data or 'test' to process testdata_phase2 when prompted.
6. The script will prompt you to confirm whether all the data files are in .txt format. Enter 'yes' or 'no'.
7. If you enter 'yes' or 'y', the script will parse the text files and build dictionaries. Once finished, it will generate an output file named `forward_index.txt` and `inverted_index.txt` in the project folder.
8. If you enter 'no' or 'n', the script will remind you to ensure all files in the specified folder path are in .txt format before proceeding.
9. After indexing is complete, the search engine will be initialized, allowing you to search for terms within the built indexes.

## Project Structure

- `main.py`: Main script to run the text parsing functionality.
- `src/`: Contains the source code for the project modules.
  - `tokenizer.py`: Module for tokenizing documents.
  - `text_parser.py`: Module for text parsing.
  - `word_dictionary.py`: Module for building the word dictionary.
  - `file_dictionary.py`: Module for building the file dictionary.
  - `forward_index.py`: Module for building the forward index.
  - `inverted_index.py`: Module for building the inverted index.
  - `search_engine.py`: Module for searching terms in the built indexes.
- `data/`: Contains the following:
  - `ft911/`: This folder contains 15 data files in `.txt` format.
  - `test_data`: This folder contains 'testdata_phase2.txt', which is used for testing the search engine.
  - `stopwordlist.txt`: A file containing a list of stopwords.
- `requirements.txt`: File containing a list of dependencies required to run the project.
- `README.md`: This file, containing information about the project.

## Contact

For any inquiries or issues regarding this project, please contact:
Manish Raghunathareddy
ManishRaghunathareddy@my.unt.edu
