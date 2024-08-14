from codebleu import calc_codebleu


def code_bleu_score(reference_code, candidate_code):
    scores = calc_codebleu([reference_code], [candidate_code], lang="java", weights=(0.25, 0.25, 0.25, 0.25))

    # Extrahiere die einzelnen Scores
    codebleu_score = scores['codebleu']
    ngram_match_score = scores['ngram_match_score']
    weighted_ngram_match_score = scores['weighted_ngram_match_score']
    syntax_match_score = scores['syntax_match_score']
    dataflow_match_score = scores['dataflow_match_score']

    # Gebe alle Scores in einem Dictionary zurück
    return {
        "codebleu": codebleu_score,
        "ngram_match_score": ngram_match_score,
        "weighted_ngram_match_score": weighted_ngram_match_score,
        "syntax_match_score": syntax_match_score,
        "dataflow_match_score": dataflow_match_score,
    }
