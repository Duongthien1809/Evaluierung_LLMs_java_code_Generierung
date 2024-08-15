import argparse
import json
import os
import threading

from scripts.evaluation import process_evaluations
from scripts.utils import save_results_as_jsonl, save_summary_as_jsonl

os.environ["TOKENIZERS_PARALLELISM"] = "true"


def calculate_average(scores):
    return sum(scores) / len(scores) if scores else 0


def summarize_results(results, count, success, evaluation_method, model_name):
    """
    Fasst die Ergebnisse der Evaluierung zusammen.
    Berechnet den durchschnittlichen Pass@k-Wert oder die durchschnittlichen Scores, je nach Evaluierungsmethode.
    """
    if evaluation_method == "pass_at_k":
        summary = results
    elif evaluation_method == "normal":
        success_rate = (success / count) if count > 0 else 0

        # Extrahieren von CodeBLEU und CodeBERT Scores
        codeBleu_scores = [result.get("code_bleu_score", {}) for result in results]
        codeBert_scores = [result.get("codeBert", {}) for result in results]
        compilable_success = [result.get("compilable", False) for result in results if result.get("compilable", False)]

        # Durchschnittliche Werte für precision, recall und f1 berechnen
        precision_scores = [score.get("precision", 0) for score in codeBert_scores]
        recall_scores = [score.get("recall", 0) for score in codeBert_scores]
        f1_scores = [score.get("f1", 0) for score in codeBert_scores]

        # Durchschnittliche Werte für CodeBLEU-Komponenten berechnen
        ngram_match_scores = [result.get("ngram_match_score", 0) for result in codeBleu_scores]
        weighted_ngram_match_scores = [result.get("weighted_ngram_match_score", 0) for result in codeBleu_scores]
        syntax_match_scores = [result.get("syntax_match_score", 0) for result in codeBleu_scores]
        dataflow_match_scores = [result.get("dataflow_match_score", 0) for result in codeBleu_scores]

        summary = {
            "model_name": model_name,
            "total_evaluated": count,
            "completion_evaluation": round(success_rate, 4),
            "compilable_evaluation": len(compilable_success) / count,
            "code_bleu_average_score": {
                "bleu_score": calculate_average([result.get("codebleu", 0) for result in codeBleu_scores]),
                "ngram_match_score": calculate_average(ngram_match_scores),
                "weighted_ngram_match_score": calculate_average(weighted_ngram_match_scores),
                "syntax_match_score": calculate_average(syntax_match_scores),
                "dataflow_match_score": calculate_average(dataflow_match_scores),
            },
            "codeBert_average_score": {
                "codeBert_average_precision": calculate_average(precision_scores),
                "codeBert_average_recall": calculate_average(recall_scores),
                "codeBert_average_f1": calculate_average(f1_scores)
            }
        }
    else:
        raise ValueError(f"Unbekannte Evaluierungsmethode: {evaluation_method}")
    return results, summary


def ensure_directory_exists(filename, model_name):
    """Stellt sicher, dass ein Verzeichnis unter './output/' mit dem Modellnamen existiert.
       Wenn nicht, wird es erstellt und der vollständige Pfad zur Datei zurückgegeben."""
    # Erstelle den vollständigen Pfad zum Verzeichnis unter './output/'
    directory = os.path.join('./output', model_name)

    # Überprüfe, ob das Verzeichnis existiert, und erstelle es bei Bedarf
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Kombiniere das Verzeichnis mit dem Dateinamen
    file_path = os.path.join(directory, filename)

    return file_path


def load_leetcode_dataset():
    data = []
    with open('leetCode_dataset.json', 'r') as file:
        for line in file:
            # Strip whitespace and commas, then load JSON
            line = line.strip().rstrip(',')
            data.append(json.loads(line))
    return data


def main(model_name, model_type, output_file, evaluation_method, max_count):
    # Load data from the improperly formatted JSON file
    data = load_leetcode_dataset()

    # Proceed with evaluation
    results, success = process_evaluations(data, model_name, model_type,
                                           evaluation_method, max_count=max_count)

    # results_with_prompt = process_evaluations_for_prompts(data, model_name, model_type, evaluation_method,
    #                                                       max_count=max_count,
    #                                                       output_file=ensure_directory_exists("prompt_" + output_file,
    #                                                                                           model_name))

    # Summarize results
    results, summary = summarize_results(results, max_count, success, evaluation_method, model_name)
    # Ensure directories exist

    if evaluation_method == "pass_at_k":
        summary_file = "./output/pass@ksum.jsonl"
    else:
        save_results_as_jsonl(results, ensure_directory_exists(output_file, model_name))
        summary_file = "./output/summary.jsonl"

    # Save results and summary
    save_summary_as_jsonl(summary, summary_file)


def start_with_terminal():
    parser = argparse.ArgumentParser(description='Evaluierung von LLMs bei der Codegenerierung')
    parser.add_argument('--model_name', type=str, required=True, help='Name oder Pfad des Modells')
    parser.add_argument('--model_type', type=str, required=True, choices=['openai', 'huggingface', 't5', 'llama'],
                        help='Typ des Modells (openai, huggingface, t5)')
    parser.add_argument('--output_file', type=str,
                        help='Pfad zur Ausgabe-JSONL-Datei, nur wenn evaluation methode ist normal')
    parser.add_argument('--evaluation_method', type=str, required=True, choices=['pass_at_k', 'normal'],
                        help='Evaluationsmethode: pass_at_k oder normal')
    parser.add_argument('--max_count', type=int, required=True,
                        help='Wert für n bei Pass@k, muss größer als k_value sein')

    args = parser.parse_args()

    main(args.model_name, args.model_type, args.output_file, args.evaluation_method, args.max_count)


# if __name__ == "__main__":
#     # Set your arguments here
#     model_name = "gemma2-9b-it"
#     model_type = "llama"  # oder 'huggingface', 't5', 'llama'
#     output_file = "output.jsonl"
#     evaluation_method = "normal"  # oder 'pass_at_k'
#     max_count = 50
#
#     main(model_name, model_type, output_file, evaluation_method, max_count)
def run_evaluation_in_thread(model_name, model_type, output_file, evaluation_method, max_count):
    thread = threading.Thread(target=main, args=(model_name, model_type, output_file, evaluation_method, max_count))
    thread.start()
    return thread


if __name__ == "__main__":
    # Set your arguments here
    evaluations = [
        {"model_name": "gpt35", "model_type": "openai", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "gpt35", "model_type": "openai", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "gemma2-9b-it", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "gemma2-9b-it", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "gemma-7b-it", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "gemma-7b-it", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "llama-3.1-70b-versatile", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},
        {"model_name": "llama-3.1-70b-versatile", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},

        {"model_name": "llama-guard-3-8b", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "llama-guard-3-8b", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "llama3-70b-8192", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "llama3-70b-8192", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "llama3-8b-8192", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "llama3-8b-8192", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "llama3-groq-70b-8192-tool-use-preview", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "llama3-groq-70b-8192-tool-use-preview", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "llama3-groq-8b-8192-tool-use-preview", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "llama3-groq-8b-8192-tool-use-preview", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},

        {"model_name": "mixtral-8x7b-32768", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "normal", "max_count": 50},
        {"model_name": "mixtral-8x7b-32768", "model_type": "llama", "output_file": "output.jsonl",
         "evaluation_method": "pass_at_k", "max_count": 50},
        # Weitere Modelle hier hinzufügen
    ]

    threads = []
    for eval_params in evaluations:
        thread = run_evaluation_in_thread(eval_params["model_name"], eval_params["model_type"],
                                          eval_params["output_file"], eval_params["evaluation_method"],
                                          eval_params["max_count"])
        threads.append(thread)

    # Warten, bis alle Threads abgeschlossen sind
    for thread in threads:
        thread.join()

    print("Alle Evaluierungen abgeschlossen.")
