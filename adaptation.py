from _lda import *


# alpha, eta, tau0, kappa, num_words
params = [0.1, 0.01, 1, 0.75, 25]


def mid(a1, a2):
    return (a1 + a2) / 2


micro, macro = main_lda()
for i in range(5):
    new_micro, new_macro = main_lda(params[0], params[1], params[2], params[3], params[4])
    while mid(new_micro, new_macro) <= mid(micro, macro):
        params[i] += params[i] * 0.1
        micro, macro = new_micro, new_macro
        new_micro, new_macro = main_lda(params[0], params[1], params[2], params[3], params[4])
    print(i, end=' ')
    print(params[i])
