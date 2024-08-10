import json
import os
import subprocess
import tempfile

import radon.complexity as cc


def analyze_code_quality(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp_file:
        temp_file.write(code.encode('utf-8'))
        temp_file_path = temp_file.name

    pylint_output = subprocess.run(
        ['pylint', temp_file_path],
        capture_output=True,
        text=True
    )

    pylint_results = pylint_output.stdout
    complexity = cc.cc_visit(code)

    os.remove(temp_file_path)

    analysis = {
        "pylint": pylint_results,
        "complexity": complexity
    }

    return analysis


def save_results_as_jsonl(results, output_file):
    with open(output_file, 'w') as file:
        for result in results:
            file.write(json.dumps(result) + '\n')
