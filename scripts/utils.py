import json
import platform
import re
import subprocess
import sys


def extract_class_body(generated_code):
    """
    Extrahiert den Inhalt der Klasse aus dem generierten Code,
    einschließlich der Import-Anweisungen, aber ohne die
    Klassendeklaration und geschweifte Klammern. Die Package-Anweisungen
    werden entfernt.
    """
    # Zerlege den Code in Zeilen
    lines = generated_code.split('\n')

    # Neue Liste für die gefilterten Zeilen
    filtered_lines = []

    # Füge nur die Zeilen hinzu, die nicht mit 'package' beginnen
    for line in lines:
        if not line.strip().startswith('package'):
            filtered_lines.append(line)

    # Kombiniere die gefilterten Zeilen zurück zu einem String
    filtered_code = '\n'.join(filtered_lines)
    return filtered_code


def insert_code_into_solution_frame_for_load_dataset(generated_code):
    """
    Fügt den generierten Code in die Rahmenklasse Solution.java ein.
    """
    class_body = extract_class_body(generated_code)
    solution_frame = """package referenz;
%s
"""
    return solution_frame % class_body


def insert_test_code_into_solution_test_frame(test_code):
    """
    Fügt den generierten Testcode in die Rahmenklasse SolutionTest.java ein.
    """
    class_body = extract_class_body(test_code)
    solution_test_frame = """package referenz;

%s
"""
    return solution_test_frame % class_body


def insert_code_into_solution_frame(generated_code):
    """
    Fügt den generierten Code in die Rahmenklasse Solution.java ein.
    """
    package_statement = "package referenz;"

    if package_statement not in generated_code:
        generated_code = f"{package_statement}\n{generated_code}"

    return generated_code


def save_results_as_jsonl(results, output_file):
    with open(output_file, 'w') as file:
        for result in results:
            file.write(json.dumps(result) + '\n')


def save_summary_as_jsonl(summary, output_file):
    with open(output_file, 'a') as file:
        file.write(json.dumps(summary) + '\n')


def extract_rahmen_code(code: str) -> str:
    lines = code.splitlines()
    output_lines = []
    inside_method = False
    inside_class = False
    brace_count = 0
    class_started = False

    for line in lines:
        stripped_line = line.strip()

        # Behalte `package`, `import` und Kommentarzeilen
        if stripped_line.startswith('package ') or stripped_line.startswith('import ') or stripped_line.startswith(
                '//'):
            output_lines.append(line)
            continue

        # Behandle den Beginn der Klasse
        if stripped_line.startswith('public class '):
            inside_class = True
            output_lines.append(line)
            class_started = True
            continue

        # Behandle den Beginn einer Methode
        if inside_class and not inside_method and 'public ' in stripped_line and '{' in stripped_line:
            output_lines.append(line)  # Die Zeile der Methode hinzufügen
            output_lines.append("        // add content here!")  # Platzhalter hinzufügen
            inside_method = True
            brace_count += stripped_line.count('{')
            continue

        # Wenn wir uns in der Methode befinden
        if inside_method:
            brace_count += stripped_line.count('{')
            brace_count -= stripped_line.count('}')

            # Wenn die Methode endet
            if brace_count == 0 and '}' in stripped_line:
                output_lines.append('        }')  # Methode beenden
                output_lines.append('}')  # Klasse beenden
                inside_method = False
                continue

        # Wenn wir das Ende der Klasse finden
        if inside_class and stripped_line == '}':
            if not inside_method:
                output_lines.append('}')  # Klasse beenden
            inside_class = False
            continue

    return '\n'.join(output_lines)


def extract_generated_code(text):
    if text is None:
        return None

    # This regex will match the entire block of Java code enclosed in triple backticks
    match = re.search(r'```[\s\S]*?```', text, re.DOTALL)

    if match:
        # Remove the enclosing backticks
        code_block = match.group(0)
        code_block = code_block.strip('```')
    else:
        # If no backticks, use the entire text
        code_block = text

    # Find the package statement and return the code from there
    package_index = code_block.find('package')
    if package_index != -1:
        code_block = code_block[package_index:]
    else:
        # If no package statement, search for import statement
        import_index = code_block.find('import')
        if import_index != -1:
            code_block = code_block[import_index:]
        else:
            # If no import statement, search for public class statement
            class_index = code_block.find('public class')
            if class_index != -1:
                code_block = code_block[class_index:]
            else:
                class_index = code_block.find('class')
                if class_index != -1:
                    code_block = code_block[class_index:]

    # Remove any text after the last closing brace
    last_brace_index = code_block.rfind('}')
    if last_brace_index != -1:
        code_block = code_block[:last_brace_index + 1]

    return code_block.strip()


def check_maven_installed():
    """Check if Maven is installed by running 'mvn -v'. Return True if installed, False otherwise."""
    try:
        subprocess.run(['mvn', '-v'], check=True, capture_output=True, text=True)
        return True
    except FileNotFoundError:
        return False


def install_maven():
    """Install Maven depending on the operating system."""
    os_type = platform.system()

    if os_type == 'Linux':
        print("Installing Maven on Linux...")
        subprocess.run(['sudo', 'apt-get', 'install', '-y', 'mvn'], check=True)
    elif os_type == 'Darwin':  # MacOS
        print("Installing Maven on MacOS...")
        subprocess.run(['brew', 'install', 'mvn'], check=True)
    elif os_type == 'Windows':
        print("Please install Maven manually from https://maven.apache.org/download.cgi")
        sys.exit(1)
    else:
        raise Exception("Unsupported OS for automatic Maven installation.")


def run_maven_build(command):
    project_directory = './project'

    # Check if Maven is installed
    if not check_maven_installed():
        print("Maven not found. Installing Maven...")
        install_maven()

    # Proceed with running the Maven command
    result = subprocess.run(
        ['mvn', 'clean', command],
        cwd=project_directory,  # Directory to run Maven command in
        capture_output=True,
        text=True
    )

    return result.returncode, result.stdout, result.stderr
