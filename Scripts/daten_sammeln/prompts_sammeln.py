import re


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
    return extract_until_follow_up(content)


if __name__ == "__main__":
    print(get_prompt_from_readme("../Daten/LeetCode/Referenzen/java/g0001_0100/s0001_two_sum/readme.md"))
