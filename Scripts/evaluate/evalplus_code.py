import ssl

from evalplus.data import get_human_eval_plus, write_jsonl

from Scripts.generate_code import generate_code

# SSL-Zertifikatsüberprüfung deaktivieren (nur für Entwicklungszwecke)
ssl._create_default_https_context = ssl._create_unverified_context

# Setze die Parameter
model_name = "Salesforce/codegen-350M-multi"
model_type = "huggingface"  # z.B. "openai" oder "huggingface"
tokenizer_name = "Salesforce/codegen-350M-multi"
dataset = get_human_eval_plus()

# Generiere Lösungen für jedes Problem im Datensatz
samples = []
for task_id, problem in dataset.items():
    prompt = problem["prompt"]
    print("Prompt: ", prompt)
    code, class_name = generate_code(model_name, model_type, tokenizer_name, prompt)
    print("code: ", code)
    samples.append(dict(task_id=task_id, solution=code))

# Speichere die generierten Lösungen in einer JSONL-Datei
write_jsonl("samples.jsonl", samples)

# Evaluiere die generierten Lösungen
