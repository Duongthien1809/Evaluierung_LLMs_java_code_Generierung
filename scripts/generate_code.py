import os

import torch
from dotenv import load_dotenv
from openai.lib.azure import AzureOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM

# Lade Umgebungsvariablen
load_dotenv()

# Setze Umgebungsvariable für MPS-Fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Initialisiere AzureOpenAI-Client
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)


def generate_code_openai(prompt: str, model: str, max_response_tokens: int = 300):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
        max_tokens=max_response_tokens
    )
    return response.choices[0].message.content


def load_model_and_tokenizer(model_name):
    model_path = f"./models/{model_name}"
    tokenizer_path = f"./tokenizers/{model_name}"

    try:
        # Lade den Tokenizer und das Modell von der Festplatte
        if not os.path.exists(model_path) or not os.path.exists(tokenizer_path):
            tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
            model = AutoModelForCausalLM.from_pretrained(model_name)
            tokenizer.save_pretrained(tokenizer_path)
            model.save_pretrained(model_path)
        else:
            tokenizer = AutoTokenizer.from_pretrained(tokenizer_path, use_fast=False)
            model = AutoModelForCausalLM.from_pretrained(model_path)
        return tokenizer, model
    except Exception as e:
        print(f"Fehler beim Laden des Tokenizers oder Modells: {e}")
        return None, None


def generate_code_huggingface(prompt, model_name):
    # Überprüfe, ob CUDA (GPU) verfügbar ist, andernfalls CPU verwenden
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Modell und Tokenizer laden
    tokenizer, model = load_model_and_tokenizer(model_name)
    if model is None or tokenizer is None:
        return "Fehler beim Laden des Modells oder Tokenizers."

    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    outputs = model.generate(inputs.input_ids, max_new_tokens=512, do_sample=True, top_k=50, top_p=0.95,
                             num_return_sequences=1, eos_token_id=tokenizer.eos_token_id)

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Rückgabe des generierten Codes
    return generated_text


def generate_code(model_name, model_type, prompt):
    if model_type == "openai":
        code = generate_code_openai(f"Generate Java code for: {prompt}", model_name)
    else:
        code = generate_code_huggingface(f"Generate Java code for: {prompt}", model_name)

    return code
