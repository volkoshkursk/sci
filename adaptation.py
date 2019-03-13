from _lda import *
from copy import copy

"""
скрипт, ппредназначенный для поиска оптимальных значений гиперпараметров
"""
# alpha, eta, tau0, kappa, num_words
params = [0.1, 0.01, 1, 0.75, 25]


def mid(a1, a2):
    """
    функция усреднения оценок метода для разных значений параметров
    :param a1:
    :param a2:
    :return:
    """
    return (a1 + a2) / 2


micro, macro = main_lda()
# TODO проверить логику
for i in range(5):
    new_micro, new_macro = main_lda(params[0], params[1], params[2], params[3], params[4])
    new_micro_right, new_macro_right = copy((new_micro, new_macro))
    a = copy(params[i])
    while mid(new_micro_right, new_macro_right) >= mid(micro, macro):
        params[i] += params[i] * 0.1
        micro, macro = new_micro_right, new_macro_right
        new_micro_right, new_macro_right = main_lda(params[0], params[1], params[2], params[3], params[4])
    new_micro_left, new_macro_left = copy((new_micro, new_macro))
    left = copy(params[i])
    params[i] = a
    while mid(new_micro_left, new_macro_left) >= mid(micro, macro):
        params[i] -= params[i] * 0.1
        micro, macro = new_micro_left, new_macro_left
        new_micro_left, new_macro_left = main_lda(params[0], params[1], params[2], params[3], params[4])
    if mid(new_micro_left, new_macro_left) <= mid(new_micro_right, new_macro_right):
        pass
    print(i, end=' ')
    print(params[i])
