import os

from dotenv import load_dotenv
from groq import Groq
from openai.lib.azure import AzureOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

# Lade Umgebungsvariablen
load_dotenv()

# Setze Umgebungsvariable für MPS-Fallback
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"

# Initialisiere AzureOpenAI-Client
openai_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2023-05-15",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

# Initialisiere Groq-Client
llama_client = Groq(
    api_key=os.getenv("GROQ_API_KEY"),
)


def generate_code_llama(prompt, model_name):
    completion = llama_client.chat.completions.create(
        model=model_name,
        messages=[{"role": "assistant", "content": prompt}],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return completion.choices[0].message.content


def generate_code_openai(prompt, model, max_response_tokens=1000):
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7,
        max_tokens=max_response_tokens
    )
    return response.choices[0].message.content


def load_tokenizer_and_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    return tokenizer, model


def generate_code_huggingface(prompt, model_name):
    tokenizer, model = load_tokenizer_and_model(model_name)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_new_tokens=1000, do_sample=True, top_k=50, top_p=0.95,
                             num_return_sequences=1, eos_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text.replace(prompt, '')


def generate_code_t5(prompt, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    t5_model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = t5_model.generate(inputs.input_ids, max_new_tokens=1000, do_sample=True, top_k=50, top_p=0.95,
                                num_return_sequences=1, eos_token_id=tokenizer.eos_token_id)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_text.replace(prompt, '')


def generate_code(model_name, model_type, prompt):
    if model_type == "openai":
        return generate_code_openai(prompt, model_name)
    elif model_type == "huggingface":
        return generate_code_huggingface(prompt, model_name)
    elif model_type == "t5":
        return generate_code_t5(prompt, model_name)
    elif model_type == "llama":
        return generate_code_llama(prompt, model_name)
    else:
        raise ValueError("Unsupported model type")
