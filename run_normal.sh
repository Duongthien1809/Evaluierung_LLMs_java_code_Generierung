#!/bin/bash

python main.py --model_name "openchat/openchat-3.5-0106" --model_type "huggingface" --tokenizer_name "openchat/openchat-3.5-0106" --output_file "result.jsonl" --evaluation_method "normal" --max_count 50
