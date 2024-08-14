import math

from scripts.generate_code import generate_code
from scripts.metricken.codeBERT import evaluate_code_with_codeBert_score
from scripts.metricken.code_bleu import code_bleu_score
from scripts.metricken.korrektheit import korrektheit_evaluate, check_compilability
from scripts.utils import insert_code_into_solution_frame


def clean_generated_code(code):
    """
    Entfernt unerlaubte Zeichen wie Backticks aus dem generierten Code und
    extrahiert den Inhalt zwischen den ersten Backticks, einschließlich der Klasse und
    ihres Inhalts bis zur schließenden Klammer. Die Import-Anweisungen werden
    beibehalten, falls vorhanden.
    """
    # Überprüfen, ob der Code zwischen Backticks steht
    start_tick = code.find('```')
    if start_tick != -1:
        end_tick = code.find('```', start_tick + 3)
        if end_tick != -1:
            code = code[start_tick + 3:end_tick].strip()
        else:
            return ""

    # Entfernen von unerlaubten Zeichen wie Backticks
    code = code.replace('`', '')

    # Finden des Startpunkts (Import oder Klassen-Definition)
    start_index = code.find('import ')
    if start_index == -1:
        start_index = code.find('class ')
    if start_index == -1:
        return ""

    code = code[start_index:]

    # Erfassen des Codes bis zur schließenden Klammer der Klasse
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
        return ""

    return code[:end_index + 1].strip()


def pass_at_k(n, c, k):
    """
    Berechnet die Pass@k-Metrik.
    """
    if k > n:
        return 1.0
    return 1 - math.comb(n - c, k) / math.comb(n, k)


def evaluate_code_compilable(cleaned_code):
    """
    Bewertet den bereinigten Code anhand der Korrektheit Kompilierbar.
    """
    return check_compilability(insert_code_into_solution_frame(cleaned_code))


def evaluate_code_correctness(cleaned_code, test_content):
    """
    Bewertet den bereinigten Code anhand der Korrektheit mit unittests.
    """
    return korrektheit_evaluate(insert_code_into_solution_frame(cleaned_code), test_content)


def evaluate_code_codeBert(cleaned_code, referenz_code):
    """
    Bewertet den bereinigten Code anhand der codeBert mit referenz code.
    """
    return evaluate_code_with_codeBert_score(referenz_code,
                                             insert_code_into_solution_frame(cleaned_code))


def evaluate_code_with_code_bleu(cleaned_code, code_content):
    """
    Bewertet den bereinigten Code mit der Code-BLEU-Metrik.
    """
    return code_bleu_score(
        insert_code_into_solution_frame(cleaned_code), code_content)


def run_pass_at_k_evaluation(task_id, model_name, model_type, prompt_content, test_content, max_value, k_value):
    """
    Führt die Pass@k-Evaluierung für n Durchläufe durch und gibt die Ergebnisse zurück.
    """
    success_count = 0
    compiler_success_count = 0

    for i in range(max_value):
        generated_code = generate_code(model_name, model_type, prompt_content)
        cleaned_code = clean_generated_code(generated_code)

        if cleaned_code:
            korrektheit_result = evaluate_code_correctness(cleaned_code, test_content)
            compiler_result = evaluate_code_compilable(cleaned_code)
            print("i: ", i)
            if any(result.get("status") == "success" for result in korrektheit_result):
                success_count += 1
            print("  success_count: ", success_count)

            # Summiere die Compiler-Ergebnisse
            if compiler_result:
                compiler_success_count += 1

    pass_k_value = pass_at_k(max_value, success_count, k_value)
    average_korrektheit_score = success_count / max_value
    average_compiler_score = compiler_success_count / max_value

    return {
        "task_id": task_id,
        "model_name": model_name,
        "model_type": model_type,
        "n_runs": max_value,
        "successful_evaluations": success_count,
        "pass_at_k": pass_k_value,
        "completion_score": average_korrektheit_score,
        "compilable_score": average_compiler_score,
    }


def run_normal_evaluation(task_id, model_name, model_type, prompt_content, code_content, test_content):
    """
    Führt eine einzelne Evaluierung des generierten Codes durch und liefert die Ergebnisse.
    """
    generated_code = generate_code(model_name, model_type, prompt_content)
    print("generated code: ", generated_code)
    cleaned_code = clean_generated_code(generated_code)
    print("cleaned_code: ", cleaned_code)

    if not cleaned_code:
        return None
    compiler_result = evaluate_code_compilable(cleaned_code)
    korrektheit_result = evaluate_code_correctness(cleaned_code, test_content)
    precision, recall, f1 = evaluate_code_codeBert(cleaned_code, code_content)
    codebleu_score = evaluate_code_with_code_bleu(cleaned_code, code_content)

    status = "success" if any(result.get("status") == "success" for result in korrektheit_result) else "failure"

    return {
        "task_id": task_id,
        "model_name": model_name,
        "model_type": model_type,
        "completion": status,
        "compilable": compiler_result,
        "code_bleu_score": codebleu_score,
        "codeBert": {
            "precision": precision,
            "recall": recall,
            "f1": f1
        },
        "count": 1

    }


def process_evaluations(data, model_name, model_type, evaluation_method, max_count=150):
    """
    Iteriert über die Eingabedaten und führt die Evaluierungen durch.
    """
    success = 0
    results = []
    count = 0

    for entry in data:
        if count >= max_count:
            break

        prompt = entry["prompt"]["problem"] + "\n" + entry["prompt"]["description"]
        task_id = entry.get("task_id")
        test_code = entry.get("test_code")

        if evaluation_method == "pass_at_k":
            result = run_pass_at_k_evaluation(task_id, model_name, model_type, prompt, test_code, max_count, 1)
            print("count: ", count)
            return result, success
        elif evaluation_method == "normal":
            referenz_code = entry.get("referenz_code")
            result = run_normal_evaluation(task_id, model_name, model_type, prompt, referenz_code, test_code)
            if result is not None:
                if result.get("completion") == "success":
                    success += 1
                    print("success: ", success)
                result.update({
                    "task_id": task_id,
                    "model_name": model_name,
                    "model_type": model_type,
                    "count": count + 1
                })
                results.append(result)
                count += 1
                print("count: ", count)

    return results, success
