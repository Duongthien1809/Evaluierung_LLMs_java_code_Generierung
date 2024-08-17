import math

from scripts.daten_sammeln.chain_prompt import CoT, ToT, Few_shot, Zero_shot
from scripts.generate_code import generate_code
from scripts.metricken.codeBERT import evaluate_code_with_codeBert_score
from scripts.metricken.code_bleu import code_bleu_score
from scripts.metricken.korrektheit import korrektheit_evaluate, check_compilability
from scripts.utils import extract_generated_code, insert_code_into_solution_frame


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
    return check_compilability(cleaned_code)


def evaluate_code_correctness(cleaned_code, test_content):
    """
    Bewertet den bereinigten Code anhand der Korrektheit mit unittests.
    """
    return korrektheit_evaluate(cleaned_code, test_content)


def evaluate_code_codeBert(cleaned_code, referenz_code):
    """
    Bewertet den bereinigten Code anhand der codeBert mit referenz code.
    """
    return evaluate_code_with_codeBert_score(referenz_code,
                                             cleaned_code)


def evaluate_code_with_code_bleu(cleaned_code, code_content):
    """
    Bewertet den bereinigten Code mit der Code-BLEU-Metrik.
    """
    return code_bleu_score(cleaned_code, code_content)


def run_pass_at_k_evaluation(technik, task_id, model_name, model_type, formatted_prompt, test_content, max_value,
                             k_value):
    """
    Führt die Pass@k-Evaluierung für n Durchläufe durch und gibt die Ergebnisse zurück.
    """
    success_count = 0
    compiler_success_count = 0
    extra_prompt_message = ""

    for i in range(max_value):
        current_prompt = formatted_prompt + "\n" + extra_prompt_message
        print(current_prompt)
        extract_code = generate_and_extract_code(model_name, model_type, current_prompt)
        print("Extracting code:\n", extract_code)
        korrektheit_result = evaluate_code_correctness(extract_code, test_content)
        compiler_result = evaluate_code_compilable(extract_code)
        print("i: ", i)
        if korrektheit_result == "success":
            success_count += 1
            extra_prompt_message = ""  # Reset the extra message if successful
        else:
            extra_prompt_message = "check more on the example and try to create code pass this scenarios!"
        print("  success_count: ", success_count)
        # Summiere die Compiler-Ergebnisse
        if compiler_result:
            compiler_success_count += 1

    pass_k_value = pass_at_k(max_value, success_count, k_value)
    average_korrektheit_score = success_count / max_value
    average_compiler_score = compiler_success_count / max_value

    return {
        "prompt_technik": technik,
        "task_id": task_id,
        "model_name": model_name,
        "model_type": model_type,
        "n_runs": max_value,
        "successful_evaluations": success_count,
        "pass_at_k": pass_k_value,
        "completion_score": average_korrektheit_score,
        "compilable_score": average_compiler_score,
    }


def run_normal_evaluation(technik, task_id, model_name, model_type, generated_code, code_content, test_content):
    """
    Führt eine einzelne Evaluierung des generierten Codes durch und liefert die Ergebnisse.
    """

    compiler_result = evaluate_code_compilable(generated_code)
    korrektheit_result = evaluate_code_correctness(generated_code, test_content)
    precision, recall, f1 = evaluate_code_codeBert(generated_code, code_content)
    codebleu_score = evaluate_code_with_code_bleu(generated_code, code_content)

    return {
        "prompt_technik": technik,
        "task_id": task_id,
        "model_name": model_name,
        "model_type": model_type,
        "completion": korrektheit_result,
        "compilable": compiler_result,
        "code_bleu_score": codebleu_score,
        "codeBert": {
            "precision": precision,
            "recall": recall,
            "f1": f1
        },
        "count": 1

    }


def process_evaluations(data, model_name, model_type, evaluation_method, technik, k_value, max_count=150):
    """
    Iteriert über die Eingabedaten und führt die Evaluierungen durch.
    """
    success = 0
    results = []
    count = 0
    for entry in data:
        if count >= max_count:
            break
        task_id = entry.get("task_id")
        test_code = entry.get("test_code")
        referenz_code = entry.get("referenz_code")
        raw_prompt = entry.get("prompt")

        formatted_prompt = create_prompt(technik, raw_prompt)
        print("prompt: ", formatted_prompt)

        if evaluation_method == "pass_at_k":
            result = run_pass_at_k_evaluation(technik, task_id, model_name, model_type, formatted_prompt,
                                              test_code,
                                              max_count, k_value=k_value)
            print("count: ", count)
            return result, success
        elif evaluation_method == "normal":
            extracted_code = generate_and_extract_code(model_name, model_type, formatted_prompt)
            print("extracted code:\n", extracted_code)
            result = run_normal_evaluation(technik, task_id, model_name, model_type, extracted_code,
                                           referenz_code,
                                           test_code)
            if result is not None:
                count += 1
                if result.get("completion") == "success":
                    success += 1
                    print("success_normal_count: ", success)
                result.update({
                    "task_id": task_id,
                    "model_name": model_name,
                    "model_type": model_type,
                    "count": count
                })
            results.append(result)
            print("count: ", count)
    return results, success


def generate_and_extract_code(model_name, model_type, formatted_prompt):
    """
    Generiert und extrahiert Code, bis ein gültiger Code gefunden wird.
    """
    while True:
        generated_code = generate_code(model_name, model_type, formatted_prompt)
        extract_code = extract_generated_code(generated_code)
        insert_to_package_frame = insert_code_into_solution_frame(extract_code)
        if extract_code is not None and extract_code != "":
            return insert_to_package_frame


def create_prompt(technik, raw_prompt):
    """
    Creates a formatted prompt based on the given technique and raw prompt data.
    """
    template_mapping = {
        "CoT": CoT,
        "ToT": ToT,
        "Few_shot": Few_shot,
        "Zero_shot": Zero_shot
    }

    prompt_template = template_mapping.get(technik)

    if technik in ["CoT", "ToT", "Few_shot"]:
        return prompt_template.format(
            rahmen_code=raw_prompt['rahmen_code'],
            prompt=raw_prompt['problem'] + "\nDescription: " + raw_prompt['description'],
            sample=raw_prompt['sample_output']
        )
    elif technik == "Zero_shot":
        return prompt_template.format(
            rahmen_code=raw_prompt['rahmen_code'],
            prompt=raw_prompt['problem'] + "\nDescription: " + raw_prompt['description']
        )
    else:
        raise ValueError(f"Invalid prompt technique: {technik}")
