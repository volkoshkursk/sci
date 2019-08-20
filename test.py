from _lda import *

import matplotlib.pyplot as plt
import matplotlib as mpl
import NB

# from gen_lda import balance_lda
from gen_clones import generate

n = 100

# widgets = [NB.progressbar.Percentage(), NB.progressbar.Bar()]
# bar = NB.progressbar.ProgressBar(widgets=widgets, max_value=n).start()


def visualisation(arr):
    for iteration in range(0, len(arr), 10):
        arr[iteration] = sorted(arr[iteration], key=lambda kv: -kv[1])
        x = []
        y = []
        for j in arr[iteration]:
            x.append(j[0])
            y.append(float(j[1]))
        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
        mpl.rcParams.update({'font.size': 9})
        plt.title('Шаг №' + str(iteration))
        plt.pie(
            y, autopct='%.1f', radius=1.1,
            explode=[0.15] + [0 for _ in range(len(x) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.12, 0.8, 0.25, 0.25),
            loc='lower left', labels=x[:5])
        fig.savefig('pic/' + str(iteration) + '.png')
        # plt.show()
        plt.clf()
        del fig
    arr[len(arr)-1] = sorted(arr[len(arr)-1], key=lambda kv: -kv[1])
    x = []
    y = []
    for j in arr[len(arr)-1]:
        x.append(j[0])
        y.append(float(j[1]))
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    plt.title('Шаг №' + str(len(arr)-1))
    plt.pie(
        y, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(x) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.12, 0.8, 0.25, 0.25),
        loc='lower left', labels=x[:5])
    fig.savefig('pic/' + str(len(arr)-1) + '.png')
    # plt.show()
    plt.clf()
    del fig


def save(*args):
    text = ''
    for i in args:
        text += str(i) + '\n'
    f = open('result', 'w')
    f.write(text)
    f.close()


if __name__ == '__main__':
    num_words = 10
    conn = sqlite3.connect('collection/collection_10.db')
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor = conn.cursor()
    num = 4
    cat, spec = get_collection_categories('reuters21578.tar', 't10')
    # для коллекции из 10 - это 10 тем
    # C = dict.fromkeys(cat[num])
    C = dict()
    for i in spec:
        cursor.execute(
            "select word from " + groupname[num] +
            " where classname== '" + i + "' order by mi desc limit " + str(num_words))
        C[i] = list(map(lambda x: x[0], cursor.fetchall()))
    cursor.execute("select * from inp where inp." + groupname[num] + "!= 'None' ")
    ddict = []
    for i in list(C.values()):
        ddict.extend(i)
    D = decode_from_db(cursor.fetchall(), cat)

#   themes = dict(sorted(sort_docs(cat[num], D).items(), key=lambda kv: -len(kv[1])))

    cursor.execute("select * from inp ")
    all_docs = decode_from_db(cursor.fetchall(), cat)

    # создаём тестовое множество
    cursor.execute("select * from test where test." + groupname[num] + "!= 'None'")
    test = decode_from_db(cursor.fetchall(), cat)

    clf_arr = []  # NB
    clf_2_arr = [list(), list(), list(), list()]
    lda_arr = [list(), list(), list(), list()]  # lda
    classes = []  # длины классов
    for i in range(n):
        print(i)
        # bar.update(i)
        train = NB.convert_sgml(D)
        print('NB single')
        clf_1 = NB.naive_Bayes(C)
        clf_1.fit(train[0], train[1])
        print('NB multi')
        clf_2 = NB.MultipleNaiveBayes(C, spec)
        clf_2.fit(train[0], train[1])
        # clf_2_arr.append(sum(estimate(clf_2.predict(test), test))/4)
        temp = estimate(clf_2.predict(test), test)
        for j in range(4):
            clf_2_arr[j].append(temp[j])

        clf_arr.append(estimate_single(clf_1.predict(test), test))
        print('LDA')
        # lda_arr.append(sum(estimate(online_lda_clf(ddict, D, all_docs, test), test))/4)

        temp = estimate(online_lda_clf(ddict, D, all_docs, test), test)

        for j in range(4):
            lda_arr[j].append(temp[j])

        classes.append(count_docs(spec, D).items())

        min_el = min(sort_docs(spec, D).items(), key=lambda x: len(x[1]))
        # del clf_1, train
        print('Update')
        # D.append(balance_lda(ddict, all_docs, min_el[0], D, cat[num]))
        themes = sort_docs(spec, D)
        D += generate(themes[min_el[0]], 1)

    # bar.finish()

    save(clf_arr, clf_2_arr, lda_arr, classes)
    plt.plot(clf_arr)
    plt.savefig('pic/NB.png', format='png', dpi=100)
    # plt.show()
    plt.clf()
    # plt.plot(lda_arr)
    # plt.savefig('pic/lda.png', format='png', dpi=100)
    for i in range(len(clf_2_arr)):
        plt.plot(clf_2_arr[i], label=str(i))
        plt.savefig('pic/MultiNB_' + str(i) + '.png', format='png', dpi=100)
        plt.clf()
    plt.clf()
    visualisation(classes)
    for i in range(len(lda_arr)):
        plt.plot(lda_arr[i], label=str(i))
        plt.savefig('pic/lda_' + str(i) + '.png', format='png', dpi=100)
        plt.clf()
    plt.clf()
    # plt.show()
    # # plt.show()
