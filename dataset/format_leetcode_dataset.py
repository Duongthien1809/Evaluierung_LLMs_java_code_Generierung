import json

from scripts.daten_sammeln.prompts_sammeln import format_problem_statement
from scripts.utils import insert_code_into_solution_frame, insert_test_code_into_solution_test_frame


def format_leetcode_dataset(json_file):
    # Daten aus der JSON-Datei laden
    with open(json_file, 'r') as file:
        data = json.load(file)

    results = []
    count, success = 0, 0

    with open('../leetcode_dataset.json', 'w') as file:
        for entry in data:
            directory = entry.get("directory", "")
            # Kürzen des Verzeichnisses
            short_directory = '/' + '/'.join(directory.split('/')[4:])
            prompts = entry.get("prompts", [])
            codes = entry.get("reference_codes", [])
            tests = entry.get("test_codes", [])

            for prompt_entry in prompts:
                prompt_content = prompt_entry["content"]

                for code_entry in codes:
                    code_content = code_entry["content"]

                    for test_entry in tests:
                        test_content = test_entry["content"]

                        # Speichern der Daten in der JSONL-Datei
                        json_line = json.dumps({
                            "task_id": short_directory,
                            "prompt": format_problem_statement(prompt_content),
                            "referenz_code": insert_code_into_solution_frame(code_content),
                            "test_code": insert_test_code_into_solution_test_frame(test_content)
                        })
                        file.write(json_line + '\n')

                        count += 1
                        print("count: ", count)
    return results


def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)


format_leetcode_dataset("leetCode_dataset.json")
