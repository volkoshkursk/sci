from _lda import *


def sort_docs(cat, D):
    """
    сортировка документов по категориям
    :param cat: список категорий
    :param D: список документов (элементы класса news)
    :return: словарь категорий, в кач-ве значений - документы соответствующей категории
    """
    themes = dict()
    for x in cat:
        for doc in D:
            if x in doc.topics_array:
                if themes.get(x) is None:
                    themes[x] = [doc]
                else:
                    themes[x] += [doc]
    return themes


def generate(theme, count):
    """
    генерация нового обучающего множества
    :param theme: список документов (элементы класса news), соответсвующих одной теме
    :param count: необходимое количество документов
    :return: список документов (элементы класса news)
    """
    if count > len(theme):
        return theme*(count - len(theme))
    else:
        return theme


def online_lda_clf(ddict, D, all_docs, test):
    """

    :param ddict:
    :param D:
    :param all_docs:
    :param test:
    :return:
    """
    alpha=0.1
    eta=0.01
    tau0=1
    kappa=0.75
    len_real_cat=15
    (matrix, vocab) = using_lda_no_changes_doc(ddict, len_real_cat, all_docs,
                                               alpha, eta, tau0, kappa)
    average = 0
    for i in matrix:
        for j in i:
            average += j
    average = average / (matrix.shape[0] * matrix.shape[1])

    translate_table = translate(len_real_cat, D, vocab, matrix, average)
    result = []
    for i in test:
        result.append(clf(bpt(i), vocab, matrix, len_real_cat, average))
    # узнаем названия классов
    result_new = []
    for i in result:
        result_new.append(set([translate_table[j] for j in i]))
    return result_new


def estimate(result, test):
    """
    замер точности (micro/macro, recall/precision)
    :param result: результат рааботы классификатора на тестовом множестве
    :param test: "правильные" ответы
    :return: 4 оценки: micro recall, micro precision, macro recall, macro precision
    """
    # замер точности для тестового множества (macro)
    result_score = 0
    total_score = 0
    total_score_ = 0
    average = 0
    average_ = 0
    real_cat = set()
    for i in test:
        real_cat.update(set(i.topics_array))

    for current_theme in real_cat:
        for i in range(len(test)):
            if current_theme in test[i].topics_array:
                if current_theme in result[i]:
                    result_score += 1
                else:
                    total_score += 1
            elif current_theme in result[i]:
                total_score_ += 1
        average += result_score / (total_score + result_score)
        if (total_score_ + result_score)!=0:
            average_ += result_score / (total_score_ + result_score)
        else:
            average_ += 0
    macro_test_r = average / len(real_cat)
    macro_test_p = average_ / len(real_cat)

    # замер точности для тестового множества (micro)
    tp = 0
    # tn = 0
    fp = 0
    fn = 0
    for i in range(len(test)):
        for theme in result[i]:
            if theme in test[i].topics_array:
                tp += 1
            else:
                fp += 1
        for theme in test[i].topics_array:
            if theme not in result[i]:
                fn += 1
    if tp + fp != 0:
        micro_test_p = tp / (tp + fp)
    else:
        micro_test_p = 0
    micro_test_r = tp / (tp + fn)
    return micro_test_p, micro_test_r, macro_test_p, macro_test_r


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
    themes = dict(sorted(sort_docs(cat[num], D).items(), key=lambda kv: -len(kv[1])))

    cursor.execute("select * from inp ")
    all_docs = decode_from_db(cursor.fetchall(), cat)

    # создаём тестово множество
    cursor.execute("select * from test where test." + groupname[num] + "!= 'None'")
    test = decode_from_db(cursor.fetchall(), cat)

    # классификатор на основе Online LDA (без балансировки)
    print(estimate(online_lda_clf(ddict, D, all_docs, test), test))

    # балансируем
    for i in themes.keys():
        D += generate(themes[i], len(themes[i]))

    # gen = generate(themes['corn'], 3987)
    # классификатор на основе Online LDA (после балансировки)
    print(estimate(online_lda_clf(ddict, D, all_docs, test), test))


if __name__ == '__main__':
    main_clones(10)
