import re

from scripts.utils import insert_test_code_into_solution_test_frame, extract_rahmen_code


def load_prompt(prompt_file):
    with open(prompt_file, 'r') as file:
        content = file.read()

    # Entfernen von Markdown-spezifischen Formatierungen
    content_as_txt = re.sub(r'^#.*', '', content, flags=re.MULTILINE)  # Entfernt Überschriften
    content_as_txt = re.sub(r'\\.', '', content_as_txt)  # Rohstring
    content_as_txt = re.sub(r'\*\*(.*?)\*\*', r'\1', content_as_txt)  # Entfernt Fettschrift
    content_as_txt = re.sub(r'\*(.*?)\*', r'\1', content_as_txt)  # Entfernt Kursivschrift
    content_as_txt = re.sub(r'_(.*?)_', r'\1', content_as_txt)  # Entfernt Kursivschrift mit Unterstrichen
    content_as_txt = re.sub(r'!\[.*?\]\(.*?\)', '', content_as_txt)  # Entfernt Bilder
    content_as_txt = re.sub(r'\[.*?\]\(.*?\)', '', content_as_txt)  # Entfernt Links komplett
    content_as_txt = re.sub(r'`{1,3}(.*?)`{1,3}', r'\1', content_as_txt)  # Behalten von Inline-Code ohne Backticks
    content_as_txt = re.sub(r'```[\s\S]*?```', '', content_as_txt)  # Entfernt Codeblöcke
    content_as_txt = re.sub(r'^>\s+', '', content_as_txt, flags=re.MULTILINE)  # Entfernt Blockzitate
    content_as_txt = re.sub(r'^\s*[-*]\s+', '', content_as_txt, flags=re.MULTILINE)  # Entfernt Listenpunkte
    content_as_txt = re.sub(r'\d+\.\s+', '', content_as_txt)  # Entfernt nummerierte Listenpunkte

    # Entfernt überschüssige Leerzeilen
    content_as_txt = re.sub(r'\n\s*\n', '\n', content_as_txt)

    return content_as_txt.strip()


def extract_until_follow_up(text):
    follow_up_marker = "Constraints"
    parts = text.split(follow_up_marker)
    if len(parts) > 1:
        return parts[0].strip()
    else:
        return text.strip()


def get_prompt_from_readme(filename: str):
    content = load_prompt(filename)
    prompt = extract_until_follow_up(content)
    return prompt


def format_problem_statement(text, test_content, reference_content):
    # Splitting the text by "\nExample " to separate examples from the rest
    parts = text.split("\nExample ")

    # Extracting problem and description
    problem_and_description = parts[0].strip()

    # Extracting the problem title (before the first newline)
    problem_title_end = problem_and_description.find("\n")
    problem_title = problem_and_description[:problem_title_end].strip()

    # Remove any leading numbers from the problem title
    problem_title = " ".join(problem_title.split(" ")[1:])

    # Everything after the first newline is the description
    description = extract_description(problem_and_description)

    # Prepend 'description: ' to the description string
    description = description

    # Sample output will be the remaining parts joined back together
    sample_output = "Example " + "\nExample ".join(parts[1:]).strip()

    # Reformat the problem title to start with "problem:"
    problem = problem_title

    # Combine all parts into the final formatted text
    formatted_text = f"{problem}\n{description}\n{sample_output}"

    # Returning the formatted text and its parts
    return {
        "problem": problem,
        "description": description,
        "sample_output": sample_output,
        "full_text": formatted_text,
        "test_content": insert_test_code_into_solution_test_frame(test_content),
        "rahmen_code": extract_rahmen_code(reference_content)
    }


def extract_description(text):
    # Find the first occurrence of "Medium", "Easy", or "Hard" in the text
    match = re.search(r"\b(Medium|Easy|Hard)\b", text)

    if match:
        # Extract description starting after the difficulty level
        description = text[match.end():].replace("\n", " ").strip()
    else:
        # If no difficulty level is found, take the whole text as the description
        description = text.replace("\n", " ").strip()

    return description
