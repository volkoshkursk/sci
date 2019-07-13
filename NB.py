import progressbar
import numpy as np
from collections import Counter
import math, re
import operator


def convert_sgml(D):
    texts = []
    classes = []
    for i in D:
        text = ''
        if i.title is not None:
            text += i.title
        if i.body is not None:
            text += i.body
        text = re.sub(r'[^a-z 0-9]', '', text.lower())
        texts.append(text)
        classes.append(i.topics_array)
    return texts, classes


def custom_sum(iterable):
    res = iterable[0]
    for i in range(1, len(iterable)):
        res += iterable[i]
    return res


def generate_boolean(y_, cond):
    res = []
    for i in y_:
        res.append(cond(i))
    return np.array(res)


class naive_Bayes:
    def __init__(self, c):
        self.c = c
        self.prior = None
        self.condprob = None

    def __get_w(self, i, j):
        a = self.condprob[i][j]
        if a is None:
            return 1
        else:
            return a

    def fit(self, x_, y_):
        if len(x_) == len(y_):
            n = len(x_)
        else:
            raise RuntimeError('Invalid arguments')
        v = set()
        [v.update(set(x)) for x in self.c.values()]  # словарь
        self.prior = dict()
        self.condprob = dict()
        widgets = [progressbar.Percentage(), progressbar.Bar()]
        bar = progressbar.ProgressBar(widgets=widgets, max_value=len(self.c.keys())).start()
        i_bar = 0
        themes_count = Counter(custom_sum(y_))
        # считаем частоты появления тем
        for i in self.c.keys():
            self.prior.update(dict.fromkeys([i], themes_count[i] / n))
            # ----------------------------------------
            text = ''
            text += ' '.join(np.array(x_)[generate_boolean(y_, lambda x: i in x)])  # собираем все тексты
            # из одной категории в один общий
            text = text.split(' ')
            # text = list(tuple(zip([''] + text, text)))
            # text = list(tuple(zip([''] + [''] + text, [''] + text, text)))
            # в text собираются тела/заголовки документов, отмеченных темой i
            # ----------------------------------------
            if len(text) == 0:
                continue
            word_count = Counter(text)  # считаем частоты слов в общем тексте
            all_ = len(text) + len(v)
            self.condprob[i] = dict()
            for x in v:
                self.condprob[i].update(
                    dict.fromkeys([x], ((word_count[x] + 1) / all_)))  # вероятность каждого слова в каждой теме
            bar.update(i_bar)
            i_bar += 1
        bar.finish()

    def use(self, d):
        if self.prior is None:
            raise RuntimeError('Model is not fitted!')
        body = ''
        if d.title is not None:
            body = d.title
        if d.body is not None:
            body += d.body
        body = re.sub(r'[^a-z 0-9]', '', body.lower())
        v = set()
        [v.update(set(x)) for x in self.c.values()]
        w = list()
        # if len(body) > 0:
        #     got_text = list(tuple(zip([''] + body, body)))
        # else:
        #     got_text = ['']
        got_text = body.split()
        # got_text = list(tuple(zip([''] + [''] + text, [''] + text, text)))
        for i in got_text:
            if i in v:
                w.append(i)
        score = dict()
        for i in self.c.keys():
            if self.prior[i] > 0:
                score.update(dict.fromkeys([i], (math.log(self.prior[i]))))
                for j in w:
                    score[i] += math.log(self.__get_w(i, j))  # self.condprob[i][j]
        return max(score.items(), key=operator.itemgetter(1))[0]

    def predict(self, arr):
        return [self.use(i) for i in arr]

    # def get_params(self, deep=True):  # Сделано только что бы cross_val_score работал
    #     return dict()

