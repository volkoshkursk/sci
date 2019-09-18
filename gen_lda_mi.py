from _lda import *
import random


def gen_mi():
    return


def balance_lda(ddict, all_docs, theme, D, cat):
    """

    :param cat:
    :param D:
    :param ddict:
    :param all_docs:
    :param theme:
    :return:
    """
    alpha = 0.1
    eta = 0.01
    tau0 = 1
    kappa = 0.75
    len_real_cat = 15
    (matrix, vocab) = using_lda_no_changes_doc(ddict, len_real_cat, all_docs,
                                               alpha, eta, tau0, kappa)

    average = 0
    for i in matrix:
        for j in i:
            average += j
    average = average / (matrix.shape[0] * matrix.shape[1])

    translate_table = translate(len_real_cat, D, vocab, matrix, average)

    lda_index = []
    start = 0
    while start < len(translate_table):
        if theme in translate_table[start:]:
            start = translate_table.index(theme, start)
            lda_index.append(start)
            start += 1
        else:
            del start
            break
    # vocab_index = dict()
    # for x in lda_index:
    #     vocab_index.update(dict(enumerate(matrix[:, x])))
    # vocab_index = dict(sorted(vocab_index.items(), key=lambda kv: -kv))

    # реализация как у Камалова
    # =========================
    result_index = []
    for x in lda_index:
        vocab_index = dict(sorted(dict(enumerate(matrix[:, x])).items(), key=lambda kv: -kv[1]))
        result_index += random.sample(list(vocab_index)[0:100], 10)
    # =========================

    # vocab_index = dict(sorted(dict(enumerate(matrix[:, lda_index])).items(), key=lambda kv: -kv[1]))

    # средняя длина документа 129.33782991202347

    # result_index = []
    # for i in range(13):
    #     result_index += random.sample(list(vocab_index)[0:100], 10)
    inversed_vocab = {value: key for key, value in vocab.items()}

    # result = [inversed_vocab[i] for i in result_index]

    result = news('YES', 'TRAIN', 'TRAINING-SET', 0, 0, None)
    result.set_body(' '.join([inversed_vocab[i] for i in result_index]))
    result.set_topics([theme], cat)
    return result


def balance_own_lda(ddict, all_docs, theme, D, cat):
    """

    :param cat:
    :param D:
    :param ddict:
    :param all_docs:
    :param theme:
    :return:
    """
    alpha = 0.1
    eta = 0.01
    tau0 = 1
    kappa = 0.75
    len_real_cat = 15
    (matrix, vocab) = using_lda_no_changes_doc(ddict, len_real_cat, all_docs,
                                               alpha, eta, tau0, kappa)

    average = 0
    for i in matrix:
        for j in i:
            average += j
    average = average / (matrix.shape[0] * matrix.shape[1])

    translate_table = translate(len_real_cat, D, vocab, matrix, average)

    lda_index = []  # список тем, созданных LDA, соответсвующих заданной теме Reuters
    start = 0
    while start < len(translate_table):
        if theme in translate_table[start:]:
            start = translate_table.index(theme, start)
            lda_index.append(start)
            start += 1
        else:
            del start
            break
    vocab_index = dict()
    for x in lda_index:
        temp = dict(enumerate(matrix[:, x]))
        # done сделать слияние словарей (если элемент есть - значение - сумма)
        for j in temp.keys():
            vocab_index[j] = vocab_index.get(j, 0) + temp[j]
        del temp

    # Roulette wheel selection
    # (https://ru.stackoverflow.com/questions/798057/Как-выбрать-одно-из-значений-с-определенной-вероятностью)

    # реализация как у Камалова
    # DONE: Можно попытаться взять то, что закомментировано и генерировать новые топики по какому-нибудь распределению
    # =========================
    # result_index = []
    # for x in lda_index:
    #     vocab_index = dict(sorted(dict(enumerate(matrix[:, x])).items(), key=lambda kv: -kv[1]))
    #     result_index += random.sample(list(vocab_index)[0:100], 10)
    # =========================

    # средняя длина документа 129.33782991202347

    result_index = []
    max_ = sum(vocab_index.values())
    for i in range(130):
        temp = random.random()
        for j in range(len(vocab_index.keys())):
            temp -= vocab_index[j]/max_
            if temp < 0:
                result_index.append(j)
                break

    inversed_vocab = {value: key for key, value in vocab.items()}

    result = news('YES', 'TRAIN', 'TRAINING-SET', 0, 0, None)
    result.set_body(' '.join([inversed_vocab[i] for i in result_index]))
    result.set_topics([theme], cat)
    return result
