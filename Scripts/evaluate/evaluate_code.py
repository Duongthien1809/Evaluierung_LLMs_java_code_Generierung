import os
import subprocess


def run_maven_build():
    project_directory = '/Users/td/Desktop/Private/BA/project/evalLLMForJavaGenerierung/project'
    result = subprocess.run(
        ['mvn', 'clean', 'install'],
        cwd=project_directory,  # Verzeichnis, in dem das Maven-Kommando ausgeführt wird
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout, result.stderr


def evaluate_code(code, test_code):
    """
    Bewertet den Code, indem er in das Maven-Projekt eingefügt, gebaut und getestet wird.

    :param code: Der zu bewertende Code als String.
    :param test_code: Der Testcode als String.
    :return: Die Ergebnisse der Tests.
    """
    results = []

    if not code or not test_code:
        raise ValueError("Kein gültiger Code zum Ausführen gefunden.")

    # Verzeichnisse sicherstellen
    solution_dir = os.path.join("project", "src", "main", "java", "referenz")
    test_dir = os.path.join("project", "src", "test", "java", "referenz")

    os.makedirs(solution_dir, exist_ok=True)
    os.makedirs(test_dir, exist_ok=True)

    # Schreibe den generierten Code in die Maven-Projektdatei
    solution_file = os.path.join(solution_dir, "Solution.java")
    with open(solution_file, 'w') as file:
        file.write(code)

    # Schreibe den Testcode in die Maven-Testdatei
    test_file = os.path.join(test_dir, "SolutionTest.java")
    with open(test_file, 'w') as file:
        file.write(test_code)

    # Führe den Maven-Bau- und Testbefehl aus
    return_code, stdout, stderr = run_maven_build()

    if return_code == 0:
        results.append({
            "status": "success",
        })
    else:
        results.append({
            "status": "failure",
        })

    return results
