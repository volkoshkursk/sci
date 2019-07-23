from _lda import *
from gen_clones import sort_docs, count_docs
import NB
import random


def balance_lda(ddict, all_docs, theme, D):
    """

    :param D:
    :param ddict:
    :param all_docs:
    :param theme:
    :param count: сколько добавить
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
    # TODO Можно попытаться взять то, что закомментировано и генерировать новые топики по какому-нибудь распределению
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

    result = [inversed_vocab[i] for i in result_index]

    return result


def main_lda_themes(num_words):
    conn = sqlite3.connect('collection_full.db')
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor = conn.cursor()
    num = 4
    cat = get_collection_categories('reuters21578.tar')
    C = dict.fromkeys(cat[num])
    for i in cat[num]:
        cursor.execute(
            "select word from " + groupname[num] +
            " where classname== '" + i + "' order by mi desc limit " + str(num_words))
        C[i] = list(map(lambda x: x[0], cursor.fetchall()))
    cursor.execute("select * from inp where inp." + groupname[num] + "!= 'None' ")
    ddict = []
    for i in list(C.values()):
        ddict.extend(i)
    D = decode_from_db(cursor.fetchall(), cat)

    # themes = dict(sorted(sort_docs(cat[num], D).items(), key=lambda kv: -len(kv[1])))

    cursor.execute("select * from inp ")
    all_docs = decode_from_db(cursor.fetchall(), cat)

    # создаём тестовое множество
    cursor.execute("select * from test where test." + groupname[num] + "!= 'None'")
    test = decode_from_db(cursor.fetchall(), cat)

    # классификатор на основе Online LDA (без балансировки)
    print('классификатор на основе Online LDA:', end=' ')
    print(estimate(online_lda_clf(ddict, D, all_docs, test), test))

    clf_1 = NB.naive_Bayes(C)
    train = NB.convert_sgml(D)
    clf_1.fit(train[0], train[1])
    print('Наивный Байесовский классификатор (после):', end=' ')
    print(estimate_single(clf_1.predict(test), test))

    # -----------------
    # balance_lda(ddict, all_docs, list(themes.keys())[1], 10, D)
    # длины классов до
    print('длины классов до:', end=' ')
    print(sorted(count_docs(cat[num], D).items(), key=lambda kv: -kv[1]))
    # балансируем
    # -----------------
    max_len = max(map(lambda x: len(x), sort_docs(cat[num], D).values()))
    min_el = min(sort_docs(cat[num], D).items(), key=lambda x: len(x[1]))
    while len(min_el[1]) < max_len:
        D += balance_lda(ddict, all_docs, min_el[0], D)
        min_el = min(sort_docs(cat[num], D).items(), key=lambda x: len(x[1]))
        print('@', end='')
    print('end')
    # -----------------
    print('длины классов после:', end=' ')
    print(sorted(count_docs(cat[num], D).items(), key=lambda kv: -kv[1]))
    print('классификатор на основе Online LDA (после):', end=' ')
    print(estimate(online_lda_clf(ddict, D, all_docs, test), test))
    clf_2 = NB.naive_Bayes(C)
    train = NB.convert_sgml(D)
    clf_2.fit(train[0], train[1])
    print('Наивный Байесовский классификатор (после):', end=' ')
    print(estimate_single(clf_2.predict(test), test))


if __name__ == '__main__':
    main_lda_themes(10)
