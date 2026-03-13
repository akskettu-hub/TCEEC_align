import re
import Levenshtein
import numpy as np
from nltk.tokenize import word_tokenize, sent_tokenize


def align_parallel_texts(source_text: str, target_text: str, use_sent_tokenize=True):
    src_text_sent_tokenized = (
        sent_tokenize_text(source_text) if use_sent_tokenize else [source_text]
    )
    target_text_sent_tokenized = (
        sent_tokenize_text(target_text) if use_sent_tokenize else [target_text]
    )

    print(
        f"n of sents in src and tgt: {len(src_text_sent_tokenized)}, {len(target_text_sent_tokenized)}"
    )

    a = word_tokenize_from_sent_list(src_text_sent_tokenized)
    b = word_tokenize_from_sent_list(target_text_sent_tokenized)

    aligned_sents = align_sents(a, b)
    aligned_by_sents_and_words = align_pairs_of_sents(aligned_sents)
    return aligned_by_sents_and_words


def word_tokenize_text(text: str):
    tokenized_text = word_tokenize(text, language="english")

    return tokenized_text


# \w+\~+\w*\~?|\'?\w+\'?\w+|\w
def re_word_tokenize_text(text: str) -> list[str]:
    return re.findall(r"\w+\~+\w*\~?|\'?\w+\'?\w+|\w", text)


def sent_tokenize_text(text: str):
    res = sent_tokenize(text, language="english")
    return res


def word_tokenize_from_sent_list(sent_list: list):
    res = []
    for sent in sent_list:
        res.append(re_word_tokenize_text(sent))

    return res


def align_sents(sent_list_a, sent_list_b):
    """
    if len(sent_list_a) != len(sent_list_b):
        print("Warning! Mismatch in number of sentences.")
        return None
    """

    res = []
    for i in range(len(sent_list_a)):
        res.append((sent_list_a[i], sent_list_b[i]))

    return res


# LLM Generated
def word_cost(w1, w2):
    return Levenshtein.distance(w1, w2) / max(len(w1), len(w2))


# LLM Generated. Implements Needleman–Wunsch alignment
def align_words(seq1, seq2):

    n, m = len(seq1), len(seq2)

    dp = [[0] * (m + 1) for _ in range(n + 1)]

    gap_cost = 1

    for i in range(1, n + 1):
        dp[i][0] = i * gap_cost

    for j in range(1, m + 1):
        dp[0][j] = j * gap_cost

    for i in range(1, n + 1):
        for j in range(1, m + 1):

            sub_cost = word_cost(seq1[i - 1], seq2[j - 1])

            dp[i][j] = min(
                dp[i - 1][j] + gap_cost,
                dp[i][j - 1] + gap_cost,
                dp[i - 1][j - 1] + sub_cost,
            )

    # backtrack

    i, j = n, m
    alignment = []

    while i > 0 or j > 0:

        if i > 0 and dp[i][j] == dp[i - 1][j] + gap_cost:
            alignment.append((seq1[i - 1], None))
            i -= 1

        elif j > 0 and dp[i][j] == dp[i][j - 1] + gap_cost:
            alignment.append((None, seq2[j - 1]))
            j -= 1

        else:
            alignment.append((seq1[i - 1], seq2[j - 1]))
            i -= 1
            j -= 1

    alignment.reverse()

    return alignment


# LLM generated
# Not used. string alignment not useful as far as I can see (Akseli)
def align_strings(a, b):
    if a is None or b is None:
        return None

    n, m = len(a), len(b)
    dp = np.zeros((n + 1, m + 1))

    for i in range(n + 1):
        dp[i][0] = i
    for j in range(m + 1):
        dp[0][j] = j

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,  # deletion
                dp[i][j - 1] + 1,  # insertion
                dp[i - 1][j - 1] + cost,  # substitution
            )

    # backtrack
    i, j = n, m
    alignment = []

    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == dp[i - 1][j] + 1:
            alignment.append((a[i - 1], None))
            i -= 1
        elif j > 0 and dp[i][j] == dp[i][j - 1] + 1:
            alignment.append((None, b[j - 1]))
            j -= 1
        else:
            alignment.append((a[i - 1], b[j - 1]))
            i -= 1
            j -= 1

    alignment.reverse()

    return alignment


def align_pairs_of_sents(aligned_sents):
    res = []
    for pair in aligned_sents:
        res.append(align_words(pair[0], pair[1]))

    return res


if __name__ == "__main__":
    with open("./data/AR-HAM-00001-00001-00001-00011-n.txt", "r") as f:
        a = f.read()

    with open("./data/AR-HAM-00001-00001-00001-00011.txt", "r") as f:
        b = f.read()

    res = align_parallel_texts(a, b, False)
    for thing in res:
        print(thing)
        print()
    """
    a = "A university has said it was recently launched new institute could put a Hampshire city at the forefront of the UK space industry. The Southampton Space Institute, which belongs to the University of Southampton, will support government plans to develop Britain's fast-growing space sector, worth £17bn every year. It brings together the expertise of world-renowned research groups and facilities to drive the development of new space technology and conversations around policy and space sustainability. Inaugural director Prof Matt Middleton said the university has taught thousands of students about aircraft and satellite design since 1959."
    b = "A univesity has said 'twas recently launch'd new institute cou'd put a Hampshire city at the forefront of the UK space industry. The Southampton Space Institute, whch belongs to the University of Southampton, will support government plans to develop Britains fast-growing space sector, worth £17bn every year. It brings together the expertise of world-renowned research groups and facilities to drive the development of new space technology and conversations around policy and space sustainability. Inaugural director Prof Matt Middleton sayd the university has taught thousands of students about aircraft and satellite design since 1959."
    res = align_parallel_texts(a, b)
    for thing in res:
        print(thing)
        print()
    """
