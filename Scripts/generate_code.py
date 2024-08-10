import os

from dotenv import load_dotenv
from openai.lib.azure import AzureOpenAI
from transformers import AutoTokenizer, AutoModelForCausalLM, T5ForConditionalGeneration

load_dotenv()

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


def generate_code_huggingface(prompt, model, tokenizer):
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048)
    position_ids = inputs.input_ids

    if position_ids.size(1) > 2048:
        raise IndexError(f"Token length {position_ids.size(1)} exceeds the maximum length of 2048")

    outputs = model.generate(
        inputs.input_ids,
        attention_mask=inputs.attention_mask,
        max_length=2048,
        pad_token_id=tokenizer.eos_token_id,
        num_return_sequences=1
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def get_class_name_from_code(code):
    for line in code.splitlines():
        if line.strip().startswith("public class"):
            parts = line.split()
            return parts[2] if len(parts) >= 3 else "Main"
    return "Main"


def generate_code(model_name, model_type, tokenizer_name, prompt):
    if model_type != "openai":
        tokenizer = AutoTokenizer.from_pretrained(tokenizer_name)

    if model_type == "t5":
        model = T5ForConditionalGeneration.from_pretrained(model_name)
    elif model_type != "openai":
        model = AutoModelForCausalLM.from_pretrained(model_name)

    if model_type == "openai":
        code = generate_code_openai(f"Generate Java code for: {prompt}", model_name)
    else:
        code = generate_code_huggingface(f"Generate Java code for: {prompt}", model, tokenizer)

    class_name = get_class_name_from_code(code)
    return code, class_name
