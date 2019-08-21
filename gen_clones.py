from _lda import *
import NB
import random

"""
Cluster-Based Over Sampling
"""


def generate(theme, count):
    """
    генерация нового обучающего множества
    :param theme: список документов (элементы класса news), соответсвующих одной теме
    :param count: необходимое количество документов
    :return: список документов (элементы класса news)
    """
    # if count > len(theme):
    #     return theme * (count - len(theme))
    # else:
    #     return theme
    if count > len(theme):
        return theme * int((count - len(theme)) / len(theme))
        # clear_theme = []
        # for i in theme:
        #     if len(i.topics_array) == 1:
        #         clear_theme.append(i)
        # if len(clear_theme) > 0:
        #     print('!')
        #     return clear_theme * int((count-len(clear_theme))/len(clear_theme))
        # else:
        #     print('?')
        #     return theme * int((count-len(theme))/len(theme))
    else:
        return random.sample(theme, count)
        # return []


def run(D, cat, num, max_len, ddict, all_docs):
    themes = dict(sorted(sort_docs(cat[num], D).items(), key=lambda kv: -len(kv[1])))
    for i in themes.keys():
        D += generate(themes[i], max_len / 2)
    return D


def main_clones(num_words):
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
    print(estimate(online_lda_clf(ddict, D, all_docs, test), test))

    # prior, condprob = NB_old.train(C, D, generate_arr_for_c(D, 4))

    clf_1 = NB.naive_Bayes(C)
    train = NB.convert_sgml(D)
    clf_1.fit(train[0], train[1])
    print(estimate_single(clf_1.predict(test), test))
    # print(estimate_single([NB_old.use(C, prior, condprob, i) for i in test], test))
    # длины классов до
    print(sorted(count_docs(cat[num], D).items(), key=lambda kv: -kv[1]))

    # балансируем
    # -----------------
    max_len = max(map(lambda x: len(x), sort_docs(cat[num], D).values()))
    D = run(D, cat, num, max_len, ddict, all_docs)

    # -----------------

    # ... и после
    print(sorted(count_docs(cat[num], D).items(), key=lambda kv: -kv[1]))
    # gen = generate(themes['corn'], 3987)
    # классификатор на основе Online LDA (после балансировки)
    print(estimate(online_lda_clf(ddict, D, all_docs, test), test))
    # prior, condprob = NB_old.train(C, D, generate_arr_for_c(D, 4))
    clf_2 = NB.naive_Bayes(C)
    train = NB.convert_sgml(D)
    clf_2.fit(train[0], train[1])
    print(estimate_single(clf_1.predict(test), test))
    # print(estimate_single([NB_old.use(C, prior, condprob, i) for i in test], test))


if __name__ == '__main__':
    main_clones(10)
