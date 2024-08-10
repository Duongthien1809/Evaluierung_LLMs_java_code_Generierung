import argparse
import json
import os

from Scripts.evaluate.evaluate_code import evaluate_code
from Scripts.evaluate.metrics import save_results_as_jsonl
from Scripts.generate_code import generate_code
from Scripts.utils import insert_code_into_solution_frame, insert_test_code_into_solution_test_frame

os.environ["TOKENIZERS_PARALLELISM"] = "false"


def clean_generated_code(code):
    """
    Entfernt unerlaubte Zeichen wie Backticks aus dem generierten Code und
    extrahiert die Klasse und ihren Inhalt bis zur schließenden Klammer.
    Die Import-Anweisungen werden beibehalten, falls vorhanden.

    :param code: Der generierte Code als String.
    :return: Bereinigter Code der Klasse und ihres Inhalts.
    """
    # Entferne unerlaubte Zeichen wie Backticks
    code = code.replace('`', '')

    # Finde den Beginn des relevanten Codes (Import-Anweisungen oder Klasse)
    start_index = code.find('import ')
    if start_index == -1:
        start_index = code.find('class ')
    if start_index == -1:
        return ""  # Keine Klasse gefunden

    # Extrahiere den Code ab dem Beginn der Imports oder Klasse
    code = code[start_index:]

    # Finde die Position des letzten schließenden geschweiften Klammerzeichens
    open_braces = 0
    end_index = -1
    for i, char in enumerate(code):
        if char == '{':
            open_braces += 1
        elif char == '}':
            open_braces -= 1
            if open_braces == 0:
                end_index = i
                break

    if end_index == -1:
        return ""  # Keine schließende Klammer gefunden

    # Extrahiere den Code bis zur schließenden Klammer
    return code[:end_index + 1].strip()


def main(model_name, model_type, tokenizer_name, output_file, json_file):
    # Lade die JSON-Datei
    with open(json_file, 'r') as file:
        data = json.load(file)

    results = []
    count = 0

    # Iteriere über die Daten in der JSON-Datei
    for entry in data:
        count += 1
        prompts = entry.get("prompts", [])
        codes = entry.get("reference_codes", [])
        tests = entry.get("test_codes", [])
        for prompt_entry in prompts:
            prompt_file = prompt_entry["file"]
            prompt_content = prompt_entry["content"]

            for code_entry in codes:
                code_file = code_entry["file"]
                code_content = code_entry["content"]

                for test_entry in tests:
                    test_file = test_entry["file"]
                    test_content = test_entry["content"]

                    # # Verarbeite die Testfälle (hier wird vorausgesetzt, dass die Testfälle in einer spezifischen Struktur vorliegen)
                    # test_cases = eval(test_content)  # Dies kann je nach Format des Inhalts angepasst werden

                    # Generiere neuen Code basierend auf dem Prompt

                    generated_code, class_name = generate_code(model_name, model_type, tokenizer_name, prompt_content)
                    # print("Generated code: ", clean_generated_code(generated_code))
                    if clean_generated_code(generated_code) != "":
                        # Bewerte den generierten Code
                        evaluation_results = evaluate_code(
                            insert_code_into_solution_frame(clean_generated_code(generated_code)),
                            insert_test_code_into_solution_test_frame(test_content))
                        # quality_analysis = analyze_code_quality(generated_code)
                        result = {
                            "model_name": model_name,
                            "model_type": model_type,
                            "tokenizer_name": tokenizer_name,
                            # "prompt_file": prompt_file,
                            # "code_file": code_file,
                            # "test_file": test_file,
                            # "generated_code": generated_code,
                            "Korrektheit": evaluation_results,
                            # "quality_analysis": quality_analysis
                        }
                        results.append(result)
        if count == 1000:
            break

    # Speichere die Ergebnisse als JSONL-Datei
    save_results_as_jsonl(results, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Evaluierung von LLMs bei der Codegenerierung')
    parser.add_argument('--model_name', type=str, required=True, help='Name oder Pfad des Modells')
    parser.add_argument('--model_type', type=str, required=True, choices=['openai', 'huggingface', 't5'],
                        help='Typ des Modells (openai, huggingface, t5)')
    parser.add_argument('--tokenizer_name', type=str, required=True, help='Name oder Pfad des Tokenizers')
    parser.add_argument('--output_file', type=str, required=True, help='Pfad zur Ausgabe-JSONL-Datei')
    parser.add_argument('--json_file', type=str, required=True, help='Pfad zur Eingabe-JSON-Datei')

    args = parser.parse_args()

    main(args.model_name, args.model_type, args.tokenizer_name, args.output_file, args.json_file)
