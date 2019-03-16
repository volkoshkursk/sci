import lda.onlineldavb as ldaO
import numpy as np
import operator
import re
import math
from base import *


def encode_words(d, ddict):
    """
    преобразует документы в наборы ид уникальных слов и их количества
    :param d: документ
    :param ddict: словарь
    :return: массив слов и их количеств
    """
    out = [list(), list()]
    for doc in d:
        out_dict = dict()
        for i in bpt(doc).translate(str.maketrans('\n', ' ')).split():
            if i in ddict:
                i = i.lower()
                i = re.sub(r'[^a-z]', '', i)
                wordtoken = ddict.index(i)
                if not (wordtoken in out_dict.keys()):
                    out_dict[wordtoken] = 0
                out_dict[wordtoken] += 1
        out[0].append(list(out_dict.keys()))
        out[1].append(list(out_dict.values()))
    return out


def get_real_cat(cat, D):
    """
    поиск категорий, которым соответсвует хоть один документ в D
    :param cat: список категорий
    :param D: список документов (элементы класса news)
    :return: список непустых категоий
    """
    out = []
    for x in cat:
        for i in D:
            if x in i.topics_array:
                out.append(x)
                break
    return out


def clf(obj, vocab_, matrix, num_of_themes, limit):
    """
    классификатор, основанный на кластеризации с помощью OnlineLDA
    :param obj: исследуемый документ
    :param vocab_: словарь из OnlineLDA
    :param matrix: матрица лямбда, генерируемая OnlineLDA
    :param num_of_themes: количество тем классификации
    :param limit: порог принадлежности документа теме
    :return:
    """
    (wordids, wordcts) = ldaO.parse_doc_list([obj], vocab_)  # TODO переписать костыль
    wordids = wordids[0]
    wordcts = wordcts[0]
    len_of_obj = sum(wordcts)
    out = []
    if len_of_obj == 0:
        return out
    score = [0 for _ in range(num_of_themes)]
    for i in range(len(wordids)):
        for j in range(num_of_themes):
            score[j] += matrix[wordids[i]][j] * wordcts[i]
    for i in range(len(score)):
        if score[i]/len_of_obj > limit:
            out.append(i)
    return out


def bpt(x):
    """
    объединение заголовка и тела новости для документа класса news
    :param x: элемент класса news
    :return: объединение заголовка и тела новости
    """
    if x.body is not None and x.title is not None:
        return x.body + x.title
    elif x.body is not None:
        return x.body
    elif x.title is not None:
        return x.title
    else:
        return ''


def using_lda_no_changes(vocab, K, D):  # TODO не работает. Исправить
    """
    вызов расчёта лямбда в реализации Online LDA с разбиением на слова "здесь"
    :param vocab: словарь (список)
    :param K: количество категорий
    :param D: коллекция документов (сисок)
    :return: параметры модели: матрица лямбда
    """
    model = ldaO.OnlineLDA(vocab, K, len(D),
                           0.1, 0.01, 1, 0.75)
    s = 10  # batch size
    docs = encode_words(D, vocab)
    for i in range(1000):
        print(i)
        wordids = [d for d in docs[0][(i * s):((i + 1) * s)]]
        wordcts = [d for d in docs[1][(i * s):((i + 1) * s)]]
        model.update_lambda(wordids, wordcts)
        np.savetxt('lambda', model._lambda)


def using_lda_no_changes_doc(vocab, K, D, alpha, eta, tau0, kappa):
    """
    вызов расчёта лямбда в реализации Online LDA с разбиением на слова на стороне Online LDA
    :param vocab: словарь (список)
    :param K: количество категорий
    :param D: коллекция документов (список)
    :param alpha: параметр модели, по умолчанию равен 0.1, его описание см. в onlineldavb.py
    :param eta: параметр модели, по умолчанию равен 0.01, его описание см. в onlineldavb.py
    :param tau0: параметр модели, по умолчанию равен 1, его описание см. в onlineldavb.py
    :param kappa: параметр модели, по умолчанию равен 0.75, его описание см. в onlineldavb.py
    :return: параметры модели: матрица лямбда и словарь (приведённый к типу для работы с Online LDA)
    """
    model = ldaO.OnlineLDA(vocab, K, len(D), alpha, eta, tau0, kappa)
#                           0.1, 0.01, 1, 0.75)
    s = math.floor(len(D)/1000)  # batch size
    docs = list(map(lambda x: bpt(x).translate(str.maketrans('\n', ' ')), D))
    for i in range(1000):
        # print(i)
        d = [d for d in docs[(i * s):((i + 1) * s)]]
        model.update_lambda_docs(d)
    d = [d for d in docs[((i + 1) * s):len(docs)]]
    model.update_lambda_docs(d)
    np.savetxt('new_lambda', model._lambda.T)
    return model._lambda.T, model._vocab


def main_lda(alpha=0.1, eta=0.01, tau0=1, kappa=0.75, num_words=150, len_real_cat=15):
    conn = sqlite3.connect('collection.db')
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
    real_cat = get_real_cat(cat[num], D)
    cursor.execute("select * from test where test." + groupname[num] + "!= 'None'")
    test = decode_from_db(cursor.fetchall(), cat)
    cursor.execute("select * from inp ")
    (matrix, vocab) = using_lda_no_changes_doc(ddict, len_real_cat, decode_from_db(cursor.fetchall(), cat),
                                               alpha, eta, tau0, kappa)
    average = 0
    for i in matrix:
        for j in i:
            average += j
    average = average / (matrix.shape[0] * matrix.shape[1])
    edu = []
    for i in D:
        edu.append(clf(bpt(i), vocab, matrix, len_real_cat, average))
    result = []
    for i in test:
        result.append(clf(bpt(i), vocab, matrix, len_real_cat, average))

    # возможно, есть способ лучше (устанавливаем соответствие между кодом темы и её названием)
    themes_as_num = [dict() for _ in range(len_real_cat)]
    for i in range(len_real_cat):
        for j in range(len(edu)):
            if i in edu[j]:
                for theme in D[j].topics_array:
                    if theme in themes_as_num[i].keys():
                        themes_as_num[i][theme] += 1
                    else:
                        themes_as_num[i][theme] = 1

    # теперь посчитаем распределение вероятностей названий тем по номерам кластеров
    for i in range(len(themes_as_num)):
        count = 0
        for j in themes_as_num[i].keys():
            count += themes_as_num[i][j]
        for j in themes_as_num[i].keys():
            themes_as_num[i][j] = themes_as_num[i][j] / count

    # построим таблицу перевода из номера кластера в название темы
    translate_table = []

    for i in range(len(themes_as_num)):
        if len(themes_as_num[i]) == 0:
            translate_table.append('None')
        else:
            translate_table.append(max(themes_as_num[i].items(), key=operator.itemgetter(1))[0])
    # for i in range(len(themes_as_num)):
    #     if len(themes_as_num[i]) == 0:
    #         translate_table.append('None')
    #     else:
    #         translate_table.append(max([j if j[0] not in translate_table else (j[0], -float('inf')) for j in
    #                                     themes_as_num[i].items()], key=operator.itemgetter(1))[0])

    # узнаем названия классов
    edu_new = []
    for i in edu:
        edu_new.append(set([translate_table[j] for j in i]))
    # print(edu_new)
    # замер точности для обучающего множества (micro)
    tp = 0
    # tn = 0
    fp = 0
    fn = 0
    for i in range(len(D)):
        for theme in edu_new[i]:
            if theme in D[i].topics_array:
                tp += 1
            else:
                fp += 1
        for theme in D[i].topics_array:
            if theme not in edu_new[i]:
                fn += 1
    micro_edu = tp/(tp+fn)
    # result_score = 0
    # total_themes = 0
    # for i in D:
    #     total_themes += len(i.topics_array)
    # for i in range(len(D)):
    #     for theme in edu_new[i]:
    #         if theme in D[i].topics_array:
    #             result_score += 1
    # print(result_score / total_themes)

    # узнаем названия классов
    result_new = []
    for i in result:
        result_new.append(set([translate_table[j] for j in i]))

    # замер точности для тренировочного множества (micro)
    tp = 0
    # tn = 0
    fp = 0
    fn = 0
    for i in range(len(test)):
        for theme in result_new[i]:
            if theme in test[i].topics_array:
                tp += 1
            else:
                fp += 1
        for theme in test[i].topics_array:
            if theme not in result_new[i]:
                fn += 1
    micro_test = tp/(tp+fn)

    # result_score = 0
    # total_themes = 0
    # for i in test:
    #     total_themes += len(i.topics_array)
    # for i in range(len(test)):
    #     for theme in result_new[i]:
    #         if theme in test[i].topics_array:
    #             result_score += 1
    # print(result_score / total_themes)
    # micro = result_score / total_themes

    # замер точности для обучающего множества (macro)
    # result_ = 0
    # del real_cat
    # for current_theme in real_cat:
    #     tp = 0
    #     fp = 0
    #     fn = 0
    #     for i in range(len(D)):
    #         if current_theme in edu_new[i]:
    #             if current_theme in D[i].topics_array:
    #                 tp += 1
    #             else:
    #                 fp += 1
    #         if current_theme in D[i].topics_array:
    #             if current_theme not in edu_new[i]:
    #                 fn += 1
    #     result_ += tp/(tp+fn)
    # macro_train = result_ / len(real_cat)
    result_score = 0
    total_score = 0
    average = 0
    for current_theme in real_cat:
        for i in range(len(D)):
            if current_theme in D[i].topics_array:
                total_score += 1
                if current_theme in edu_new[i]:
                    result_score += 1
        average += result_score/total_score
    macro_train = average / len(real_cat)

    # замер точности для тренировочного множества (macro)
    # result_ = 0
    # del real_cat
    # real_cat = set()
    # for i in test:
    #     real_cat.update(set(i.topics_array))
    #
    # for current_theme in real_cat:
    #     tp = 0
    #     fp = 0
    #     fn = 0
    #     for i in range(len(test)):
    #         if current_theme in result_new[i]:
    #             if current_theme in test[i].topics_array:
    #                 tp += 1
    #             else:
    #                 fp += 1
    #         if current_theme in test[i].topics_array:
    #             if current_theme not in result_new[i]:
    #                 fn += 1
    #     result_ += tp/(tp+fn)
    # macro_test = result_ / len(real_cat)

    result_score = 0
    total_score = 0
    average = 0
    del real_cat
    real_cat = set()
    for i in test:
        real_cat.update(set(i.topics_array))

    for current_theme in real_cat:
        for i in range(len(test)):
            if current_theme in test[i].topics_array:
                total_score += 1
                if current_theme in result_new[i]:
                    result_score += 1
        average += result_score/total_score
    macro_test = average / len(real_cat)
    # print(edu)
    # print(result)
    print('\n')
    print(micro_edu)
    print(micro_test)
    print(macro_train)
    print(macro_test)
    return micro_edu, micro_test, macro_train, macro_test


if __name__ == "__main__":
    main_lda()
