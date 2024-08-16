import code_bert_score


def evaluate_code_with_codeBert_score(reference_code, candidate_code):
    scores = code_bert_score.score(cands=[candidate_code], refs=[reference_code], lang='java')
    precision = scores[0].mean().item()
    recall = scores[1].mean().item()
    f1 = scores[2].mean().item()
    return precision, recall, f1

# # Beispiel-Referenz- und Kandidatencode
# reference_code = "public class Example { public static void main(String[] args) { System.out.println('Hello, World!'); } }"
# candidate_code = "public class Example { public static void main(String[] args) { System.out.println('Hello, World!'); } }"
#
# # Berechnung des CodeBERTScores
# precision, recall, f1 = evaluate_code_with_codeBert_score(reference_code, candidate_code)
# print(f"CodeBERTScore Ergebnisse:\nPräzision: {precision:.4f}\nRecall: {recall:.4f}\nF1-Score: {f1:.4f}")
