from _lda import *
from gen_clones import sort_docs

import matplotlib.pyplot as plt
import NB

from gen_lda import balance_lda

n = 100

# widgets = [NB.progressbar.Percentage(), NB.progressbar.Bar()]
# bar = NB.progressbar.ProgressBar(widgets=widgets, max_value=n).start()


num_words = 1
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

clf_arr = []  # NB
clf_2_arr = []
lda_arr = []  # lda
classes = []  # длины классов
for i in range(n):
    print(i)
    # bar.update(i)
    clf_1 = NB.naive_Bayes(C)
    train = NB.convert_sgml(D)
    clf_1.fit(train[0], train[1])
    # clf_2 = NB.MultipleNaiveBayes(C, cat[4])
    # clf_2.fit(train[0], train[1])
    # clf_2_arr.append(sum(estimate(clf_2.predict(test), test))/4)
    clf_arr.append(estimate_single(clf_1.predict(test), test))
    lda_arr.append(sum(estimate(online_lda_clf(ddict, D, all_docs, test), test))/4)
    # classes.append(count_docs(cat[num], D).items())

    min_el = min(sort_docs(cat[num], D).items(), key=lambda x: len(x[1]))
    del clf_1, train
    D.append(balance_lda(ddict, all_docs, min_el[0], D, cat[num]))

# bar.finish()

plt.plot(clf_arr)
plt.savefig('pic/NB.png', format='png', dpi=100)
# plt.show()
plt.clf()
plt.plot(lda_arr)
plt.savefig('pic/lda.png', format='png', dpi=100)
# plt.show()
plt.clf()
# plt.plot(clf_2_arr)
# plt.savefig('pic/MultiNB.png', format='png', dpi=100)
# # plt.show()
# plt.clf()
