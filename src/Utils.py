# Utils.py


def extract_number(doc_no):
    parts = doc_no.split("-")
    if len(parts) > 1:
        return int(parts[1])
    else:
        return int(parts[0])


def parse_topics_file(topics_file):
    """
    Parse the topics.txt file and extract query information.

    Args:
    - topics_file (str): Path to the topics.txt file.

    Returns:
    - dict: A dictionary containing query information.
      The keys are topic numbers, and the values are dictionaries
      containing 'title', 'description', and 'narrative' for each topic.
    """
    query_info = {}

    with open(topics_file, "r") as file:
        current_topic = None
        current_query = {}
        current_field = None
        for line in file:
            line = line.strip()
            if line.startswith("<num>"):
                # Extract topic number
                current_topic = line.split(":")[-1].strip()
                current_query = {}
                current_field = None  # Reset current_field for each topic
            elif line.startswith("<title>"):
                # Extract query title
                current_query["title"] = line[len("<title>") :].strip()
            elif line.startswith("<desc>"):
                # Extract query description (multiline)
                current_field = "description"
                current_query[current_field] = ""
            elif line.startswith("<narr>"):
                # Extract query narrative (multiline)
                current_field = "narrative"
                current_query[current_field] = ""
            elif line.startswith("</top>"):
                # End of current topic, store query information
                query_info[current_topic] = current_query
                current_topic = None
            elif line.startswith("<top>"):
                # Skip <top> tag
                continue
            else:
                # Add line to the current field
                if current_field:
                    current_query[current_field] += line.strip() + " "

    return query_info


def parse_qrels_file(qrels_file):
    """
    Parse the main.qrels file and extract relevance judgments.

    Args:
    - qrels_file (str): Path to the main.qrels file.

    Returns:
    - dict: A dictionary containing relevance judgments for each topic.
      The keys are topic numbers, and the values are dictionaries
      containing document names and their relevance judgments.
    """
    relevance_info = {}

    with open(qrels_file, "r") as file:
        for line in file:
            topic, _, document, relevance = line.strip().split()
            if topic not in relevance_info:
                relevance_info[topic] = {}
            relevance_info[topic][document] = int(relevance)

    return relevance_info


def calculate_precision_recall(retrieved_docs, relevant_docs):
    num_relevant_retrieved = len(set(retrieved_docs) & set(relevant_docs))
    precision = (
        num_relevant_retrieved / len(retrieved_docs) if len(retrieved_docs) > 0 else 0
    )
    recall = (
        num_relevant_retrieved / len(relevant_docs) if len(relevant_docs) > 0 else 0
    )
    return precision, recall
