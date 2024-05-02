# Text Parser Project

This project focuses on implementing a Query Processor for information retrieval, specifically targeting query processing and retrieval using the Vector Space Model (VSM) with Cosine Similarity as the relevance measure. It includes functionality for building the necessary indexes, calculating TF*IDF weights, and evaluating system performance based on Precision and Recall metrics.

## How to Run the Code

1. Ensure you have Python installed on your system.
2. Create a virtual environment in your local machine.
   `python -m venv venv`
   Activate virtual environment
   `source venv/bin/activate` # On Linux/Mac
   `venv\Scripts\activate` # On Windows
3. Install the required dependencies by running: `pip install -r requirements.txt`
4. Run the `main.py` script.
5. Follow the prompts to process the TREC data.
6. The script will prompt you to confirm whether all the data files are in .txt format. Enter 'yes' or 'no'.
7. The script will parse the text files, build the necessary indexes, and generate output files.
10. `1_vsm_output_title_desc.txt` - Relevant documents using title + Description.
    `1_vsm_output_title_narr.txt` - Relevant documents using title + narrative.
    `1_vsm_output_title.txt` - Relevant documents using title. 
    `forward_index.txt` - contains file ID : word (frequency).
    `inverted_index.txt` - contains stemmed word : File name (frequency).

## Project Structure

- `main.py`: Main script to execute the query processing functionality.
- `src/`: Contains the source code for the project modules.
  - `tokenizer.py`: Module for tokenizing documents.
  - `text_parser.py`: Module for parsing text and building dictionaries.
  - `dictionary.py`: Module for building the word and file dictionaries.
  - `index.py`: Module for building the inverted index.
  - `search.py`: Module for searching terms in the built indexes.
  - `Utils.py`: Utility functions for parsing files and calculating metrics.
- `data/`: Contains the following:
  - `ft911/`: This folder contains 15 data files in `.txt` format.
  - `stopwordlist.txt`: A file containing a list of stopwords.
  - `main.qrels`: File containing relevance judgments for each topic.
  - `topics.txt`: File containing queries for retrieval.
- `output/`: Folder containing output files generated during execution.
  - `1_vsm_output_title_desc.txt`
  - `1_vsm_output_title_narr.txt`
  - `1_vsm_output_title.txt`
  - `2_inverted_index.txt`
  - `3_forward_index.txt`
- `requirements.txt`: File containing a list of dependencies required to run the project.
- `README.md`: This file, containing information about the project.

## Contact

For any inquiries or issues regarding this project, please contact:
Manish Raghunathareddy
ManishRaghunathareddy@my.unt.edu
