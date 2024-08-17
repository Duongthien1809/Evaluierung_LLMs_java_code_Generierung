# Data erklären
`data` erhält pass@k und normals, denen Evaluierungergebnisse nach jede prompttechnik, welche sind CoT, ToT, Zero_shot, Few_shot
## pass@k
erhalten completion_score: score von Generierten code, welche sich alle unittests passen, 
compilable score: score welche generierten code kompilierbar ist und pass_at_k ist score von pass@1, 
succesfull_evaluation: anzahl von generierten code, welch unittests passen.
## normals
erhalten 
prompt_technik     object: prompt technik
model_name         object: 
Compilable        float64: compilable score: score welche generierten code kompilierbar ist
Completion        float64: completion_score: score von Generierten code, welche sich alle unittests passen
BLEU-Score        float64: codebeu score, welche Verhältnis zwischen generierten code mit referenz code nach codebleu Metrik halten
Bert-Precision    float64: CodeBert Precision, welche Verhältnis zwischen generierten code mit referenz code nach codebert score Metrik halten
Bert-Recall       float64
Bert-F1           float64

weitere Informationen:
## CodeBERT.
**Beschreibung**: Eine automatische Bewertungsmetrik für Code, basierend auf BERTScore. Sie verwendet vortrainierte kontextuelle Einbettungen, um die Ähnlichkeit zwischen generiertem und Referenzcode zu bewerten.

Die Ergebnisse, die du von CodeBERTScore erhalten hast, dienen dazu, die Qualität des generierten Codes im Vergleich zum Referenzcode zu bewerten. Hier ist eine kurze Erklärung, wofür die einzelnen Metriken stehen:

1. **Präzision (Precision)**:
    - **Bedeutung**: Misst den Anteil der relevanten Elemente unter den abgerufenen Elementen. In diesem Kontext bedeutet es, wie viele der generierten Code-Token korrekt sind im Vergleich zu den Referenz-Token.
    - **Beispiel**: Wenn der generierte Code viele korrekte Token enthält, aber auch viele falsche, wäre die Präzision niedriger.
2. **Recall**:
    - **Bedeutung**: Misst den Anteil der relevanten Elemente, die abgerufen wurden. Hier bedeutet es, wie viele der relevanten Token aus dem Referenzcode im generierten Code enthalten sind.
    - **Beispiel**: Wenn der generierte Code alle wichtigen Teile des Referenzcodes enthält, aber auch zusätzliche irrelevante Teile, wäre der Recall hoch, aber die Präzision könnte niedriger sein.
3. **F1-Score**:
    - **Bedeutung**: Das harmonische Mittel von Präzision und Recall. Es bietet eine ausgewogene Bewertung, die sowohl die Genauigkeit als auch die Vollständigkeit des generierten Codes berücksichtigt.
    - **Beispiel**: Ein hoher F1-Score bedeutet, dass der generierte Code sowohl präzise als auch vollständig ist.

## CodeBleu

- **codebleu (CodeBLEU-Score)**:
    - **Beschreibung**: Der CodeBLEU-Score ist eine angepasste Version des BLEU-Scores, die speziell für die Bewertung von generiertem Programmcode entwickelt wurde. Während der klassische BLEU-Score nur die Übereinstimmung von n-Grammen zwischen Referenz- und Zieltexten misst, berücksichtigt der CodeBLEU-Score zusätzlich sprachspezifische Merkmale wie Syntax und Datenfluss.
    - **Zweck**: Dieser Score dient dazu, die Ähnlichkeit zwischen dem generierten Code und dem Referenzcode zu bewerten, wobei sowohl die Struktur als auch die Semantik des Codes berücksichtigt werden.
