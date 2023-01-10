import re

digit_reps = {}
digit_reps["0"] = " zero "
digit_reps["1"] = " one "
digit_reps["2"] = " two "
digit_reps["3"] = " three "
digit_reps["4"] = " four "
digit_reps["5"] = " five "
digit_reps["6"] = " six "
digit_reps["7"] = " seven "
digit_reps["8"] = " eight "
digit_reps["9"] = " nine "


def levenshtein(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current = list(range(n+1))
    for i in range(1, m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1, n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)

    return current[n]

def wer(y_hat, y_ref):
    y_hat_list = y_hat.split()
    y_ref_list = y_ref.split()
    return levenshtein(y_hat_list, y_ref_list)/len(y_ref_list)

def cer(y_hat, y_ref):
    return levenshtein(y_hat, y_ref)/len(y_ref)

def convert_text(txt):
    return re.sub(r'\W+', '', txt.replace(' ', '_')).replace('_', ' ').lower()

def digitsrep(txt):
    for i in range(0, 10):
        txt = txt.replace(str(i), digit_reps[str(i)])
    return txt
