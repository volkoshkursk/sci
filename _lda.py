import lda.onlineldavb as ldaO
import numpy as np
import re
from base import *


def encode_words(d, ddict):
    """
    преобразует документы в наборы ид уникальных слов и их количества
    :param d: документ
    :param ddict: словарь
    :param C: словарь по категориям
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
    out = []
    for x in cat:
        for i in D:
            if x in i.topics_array:
                out.append(x)
                break
    return out


def clf(obj, vocab_, matrix):
    (wordids, wordcts) = ldaO.parse_doc_list([obj], vocab_)  # TODO переписать костыль
    wordids = wordids[0]
    wordcts = wordcts[0]
    score = [0 for _ in range(117)]  # TODO переписать костыль (количество тем должно загружаться автоматически)
    for i in range(len(wordids)):
        for j in range(117):  # TODO переписать костыль (количество тем должно загружаться автоматически)
            score[j] += matrix[wordids[i]][j] * wordcts[i]
    return np.argmax(score)  # TODO сделать порог добавления темы


def bpt(x):
    if x.body is not None and x.title is not None:
        return x.body + x.title
    elif x.body is not None:
        return x.body
    elif x.title is not None:
        return x.title
    else:
        return ''


def using_lda_no_changes(vocab, K, D):
    model = ldaO.OnlineLDA(vocab, K, len(D),
                           0.1, 0.01, 1, 0.75)
    s = 10  # batch size
    docs = encode_words(D, vocab)
    for i in range(1000):
        print(i)
        wordids = [d for d in docs[0][(i * s):((i + 1) * s)]]
        wordcts = [d for d in docs[1][(i * s):((i + 1) * s)]]
        model.update_lambda(wordids, wordcts)
        np.savetxt('lambda' , model._lambda)


def using_lda_no_changes_doc(vocab, K, D):
    model = ldaO.OnlineLDA(vocab, K, len(D),
                           0.1, 0.01, 1, 0.75)
    s = 9  # batch size
    docs = list(map(lambda x: bpt(x).translate(str.maketrans('\n', ' ')), D))
    for i in range(1000):
        print(i)
        d = [d for d in docs[(i * s):((i + 1) * s)]]
        model.update_lambda_docs(d)
    # np.savetxt('lambda', model._lambda.T)
    return model._lambda.T, model._vocab


def main_lda():
    conn = sqlite3.connect('collection_test_topics.db')
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor = conn.cursor()
    num = 4
    cat = get_collection_categories('reuters21578.tar')
    C = dict.fromkeys(cat[num])
    for i in cat[num]:
        cursor.execute(
            "select word from " + groupname[num] + " where classname== '" + i + "' order by mi desc limit 10")
        C[i] = list(map(lambda x: x[0], cursor.fetchall()))
    cursor.execute("select * from inp where inp." + groupname[num] + "!= 'None' ")
    ddict = []
    for i in list(C.values()):
        ddict.extend(i)
    (D, D_c) = decode_from_db(cursor.fetchall(), cat, num)
    real_cat = get_real_cat(cat[num], D)
    (matrix, vocab) = using_lda_no_changes_doc(ddict, len(real_cat), D)
    cursor.execute("select * from test where test." + groupname[num] + "!= 'None'  limit 10")
    D = decode_from_db(cursor.fetchall(), cat)

    for i in D:
        print(clf(bpt(i), vocab, matrix))


if __name__ == "__main__":
    main_lda()
