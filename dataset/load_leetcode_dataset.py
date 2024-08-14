import json
import os

from scripts.daten_sammeln.prompts_sammeln import get_prompt_from_readme
from scripts.utils import find_files


def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


def load_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def main():
    reference_results = []
    test_results = []

    # Dictionary um Verzeichnisse den Dateipfaden zuzuordnen
    reference_directories = {}
    test_directories = {}

    # Gruppiere Referenzdateien nach Verzeichnissen und Typen
    for prompt_file in find_files('./dataset/LeetCode/Referenzen/', specific_file_name="readme.md"):
        directory = os.path.dirname(prompt_file)
        if directory not in reference_directories:
            reference_directories[directory] = {"prompts": [], "reference_codes": []}
        reference_directories[directory]["prompts"].append(prompt_file)

    for code_file in find_files('./dataset/LeetCode/Referenzen/', file_exts=['Solution.java']):
        directory = os.path.dirname(code_file)
        if directory not in reference_directories:
            reference_directories[directory] = {"prompts": [], "reference_codes": []}
        reference_directories[directory]["reference_codes"].append(code_file)

    # Gruppiere Testdateien nach Verzeichnissen und Typen
    for test_file in find_files('./dataset/LeetCode/Tests/', file_exts=['SolutionTest.java']):
        directory = os.path.dirname(test_file)
        if directory not in test_directories:
            test_directories[directory] = {"test_codes": []}
        test_directories[directory]["test_codes"].append(test_file)

    # Verarbeite und speichere die Referenzcodes
    for directory, files in reference_directories.items():
        directory_result = {
            "directory": directory,
            "prompts": [],
            "reference_codes": []
        }

        # Verarbeite Prompts
        for prompt_file in files.get("prompts", []):
            prompt = get_prompt_from_readme(prompt_file)
            directory_result["prompts"].append({"file": prompt_file, "content": prompt})

        # Verarbeite Referenz-Codes
        for code_file in files.get("reference_codes", []):
            code_content = open(code_file, 'r').read()
            directory_result["reference_codes"].append({"file": code_file, "content": code_content})

        reference_results.append(directory_result)

    # Verarbeite und speichere die Testcodes
    for directory, files in test_directories.items():
        directory_result = {
            "directory": directory,
            "test_codes": []
        }

        # Verarbeite Test-Cases
        for test_file in files.get("test_codes", []):
            test_code_content = open(test_file, 'r').read()
            directory_result["test_codes"].append({"file": test_file, "content": test_code_content})

        test_results.append(directory_result)

    # Speichere die Ergebnisse als separate JSON-Dateien
    save_json(reference_results, "reference_results.json")
    save_json(test_results, "test_results.json")

    # Lade die JSON-Dateien und führe sie zusammen
    reference_data = load_json("reference_results.json")
    test_data = load_json("test_results.json")

    # Zusammenführen der dataset basierend auf dem Verzeichnisnamen
    merged_results = []
    for ref in reference_data:
        for test in test_data:
            if ref["directory"].split('/')[-1] == test["directory"].split('/')[-1]:
                merged_result = ref
                merged_result["test_codes"] = test["test_codes"]
                merged_results.append(merged_result)
                break

    # Speichere die zusammengeführten Ergebnisse als JSON-Datei
    save_json(merged_results, "leetCode_dataset.json")

    print("Ergebnisse wurden in merged_results.json gespeichert.")


if __name__ == "__main__":
    main()
