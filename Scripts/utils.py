def extract_class_body(generated_code):
    """
    Extrahiert den Inhalt der Klasse aus dem generierten Code,
    einschließlich der Import-Anweisungen, aber ohne die
    Klassendeklaration und geschweifte Klammern. Die Package-Anweisungen
    werden entfernt.

    :param generated_code: Der generierte Code als String.
    :return: Der Inhalt der Klasse als String, einschließlich der Import-Anweisungen.
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


def insert_code_into_solution_frame(generated_code):
    """
    Fügt den generierten Code in die Rahmenklasse Solution.java ein.

    :param generated_code: Der generierte Code als String.
    :return: Vollständiger Code für Solution.java.
    """
    class_body = extract_class_body(generated_code)
    solution_frame = """package referenz;
%s
"""
    return solution_frame % class_body


def insert_test_code_into_solution_test_frame(test_code):
    """
    Fügt den generierten Testcode in die Rahmenklasse SolutionTest.java ein.

    :param test_code: Der Testcode als String.
    :return: Vollständiger Code für SolutionTest.java.
    """
    class_body = extract_class_body(test_code)
    solution_test_frame = """package referenz;

%s
"""
    return solution_test_frame % class_body
