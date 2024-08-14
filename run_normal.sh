#!/bin/bash

python main.py --model_name "openchat/openchat-3.5-0106" --model_type "huggingface" --tokenizer_name "openchat/openchat-3.5-0106" --output_file "./output/openchat/openchat-3.5-0106_normal.jsonl" --json_file "leetCode_dataset.json" --evaluation_method "normal" --max_count 50
