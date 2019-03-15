from errors import *
import sqlite3
from ctypes import *
from all_skips import *
import os


"""
базовая библиотека для проекта(описание класса + некоторые методы работы с sgml в sql базе данных)
"""


class news:
    """
    класс новостей для классификатора
    названия переменных совпадают с названиями в sgml формате
    """

    def __init__(self, topics, lewissplit, cgisplit, oldid, newid, csecs):
        self.oldid = oldid
        self.newid = int(newid)
        self.lewissplit = lewissplit
        self.cgisplit = cgisplit
        if csecs == 'None':
            self.csecs = None
        else:
            self.csecs = csecs
        self.topics = topics
        self.date = None
        self.topics_array = []
        self.mknote = None
        self.places = []
        self.people = []
        self.orgs = []
        self.exchanges = []
        self.companies = None
        self.unknown = None
        self.text_type = 'NORM'
        self.author = None
        self.dateline = None
        self.title = None
        self.text_waste = None
        self.body = None

    def set_date(self, date):
        self.date = date

    def set_topics(self, topics, ctrl):  # topics - массив, ctrl - контрольное множество(set)
        """
        установить поле topics
        :param topics: список значений
        :param ctrl: контрольное множество (допустимые значения)(set)
        если передаётся значение не из множества вызывается исключение breakedCollection
        """
        if not ((len(topics) == 1) and (topics[0] == '')) and set(topics).issubset(ctrl):
            self.topics_array = topics
        elif not (set(topics).issubset(ctrl) or ((len(topics) == 1) and (topics[0] == ''))):
            print(topics)
            raise breakedCollection

    def set_mknote(self, mknote):
        if mknote != '':
            self.mknote = mknote

    def set_places(self, places, ctrl):  # places - массив, ctrl - контрольное множество(set)
        """
        установить поле places
        :param places: список значений
        :param ctrl: контрольное множество (допустимые значения)(set)
        если передаётся значение не из множества вызывается исключение breakedCollection
        """
        if not ((len(places) == 1) and (places[0] == '')) and set(places).issubset(ctrl):
            self.places = places
        elif not (set(places).issubset(ctrl) or ((len(places) == 1) and (places[0] == ''))):
            print(places)
            raise breakedCollection

    def set_orgs(self, orgs, ctrl):  # orgs - массив, ctrl - контрольное множество(set)
        """
        установить поле orgs
        :param orgs: список значений
        :param ctrl: контрольное множество (допустимые значения)(set)
        если передаётся значение не из множества вызывается исключение breakedCollection
        """
        if not ((len(orgs) == 1) and (orgs[0] == '')) and set(orgs).issubset(ctrl):
            self.orgs = orgs
        elif not (set(orgs).issubset(ctrl) or ((len(orgs) == 1) and (orgs[0] == ''))):
            print(orgs)
            raise breakedCollection

    def set_people(self, people, ctrl):  # people - массив, ctrl - контрольное множество(set)
        """
        установить поле people
        :param people: список значений
        :param ctrl: контрольное множество (допустимые значения)(set)
        если передаётся значение не из множества вызывается исключение breakedCollection
        """
        if not ((len(people) == 1) and (people[0] == '')) and set(people).issubset(ctrl):
            self.people = people
        elif not (set(people).issubset(ctrl) or ((len(people) == 1) and (people[0] == ''))):
            print(people)
            raise breakedCollection

    def set_exchanges(self, exchanges, ctrl):  # exchanges - массив, ctrl - контрольное множество(set)
        """
        установить поле exchanges
        :param exchanges: список значений
        :param ctrl: контрольное множество (допустимые значения)(set)
        если передаётся значение не из множества вызывается исключение breakedCollection
        """
        if not ((len(exchanges) == 1) and (exchanges[0] == '')) and set(exchanges).issubset(ctrl):
            self.exchanges = exchanges
        elif not (set(exchanges).issubset(ctrl) or ((len(exchanges) == 1) and (exchanges[0] == ''))):
            print(exchanges)
            raise breakedCollection

    def set_companies(self, companies):
        if len(companies) > 0 and companies != 'None':
            self.companies = companies

    def set_unknown(self, unknown):
        if len(unknown) > 0:
            self.unknown = unknown

    def set_text_type(self, type_):
        if len(type_) > 0:
            self.text_type = type_

    def set_text_waste(self, waste):
        if len(waste) > 0 and self.text_waste is None:
            self.text_waste = waste
        elif len(waste) > 0 and self.text_waste is not None:
            self.text_waste += waste

    def set_body(self, body):
        if len(body) > 0 and self.body is None:
            self.body = body
        elif len(body) > 0 and self.body is not None:
            self.body += body

    def set_title(self, title):
        if len(title) > 0 and self.title is None:
            self.title = title
        elif len(title) > 0 and self.title is not None:
            self.title += title

    def set_author(self, author):
        if len(author) > 0:
            self.author = author

    def set_dateline(self, dateline):
        if len(dateline) > 0:
            self.dateline = dateline

    def show(self):
        """
        метод вывода на экран всех значений полей объекта
        """
        print('OLDID: ' + str(self.oldid), end=' | ')
        print('NEWID: ' + str(self.newid), end=' | ')
        print('LEWISSPLIT: ' + str(self.lewissplit), end=' | ')
        print('CGISPLIT: ' + str(self.cgisplit), end=' | ')
        print('CSECS: ' + str(self.csecs), end=' | ')
        print('TOPICS: ' + str(self.topics))
        print('topics array: ' + str(self.topics_array))
        print('date: ' + str(self.date))
        if self.mknote is not None:
            print('mknote: ' + str(self.mknote))
        print('places: ' + str(self.places))
        if self.people is not None:
            print('people: ' + str(self.people))
        if self.orgs is not None:
            print('orgs: ' + str(self.orgs))
        if self.exchanges is not None:
            print('exchanges: ' + str(self.exchanges))
        if self.companies is not None:
            print('companies: ' + str(self.companies))
        if self.unknown is not None:
            print('unknown: ' + str(self.unknown))
        print('text_type: ' + str(self.text_type))
        if self.text_waste is not None:
            print('text waste: ' + str(self.text_waste))
        if self.author is not None:
            print('author: ' + str(self.author))
        if self.dateline is not None:
            print('dateline: ' + str(self.dateline))
        if self.title is not None:
            print('title: ' + str(self.title))
        print(self.body)

    def generate_string(self):
        """
        :return: строка значений, для передачи в SQL запрос
        """
        return "'" + str(self.oldid) + "'" + ',' + str(self.newid) + ',' + "'" + str(
            self.lewissplit) + "'" + ',' + "'" + str(self.cgisplit) + "'" + ',' + "'" + str(
            self.csecs) + "'" + ',' + "'" + str(self.topics) + "'" + ',' + "'" + str(
            self.date) + "'" + ',' + "'" + encode_arr(self.topics_array) + "'" + ',' + "'" + str(
            self.mknote) + "'" + ',' + "'" + encode_arr(self.places) + "'" + ',' + "'" + encode_arr(
            self.people) + "'" + ',' + "'" + encode_arr(self.orgs) + "'" + ',' + "'" + encode_arr(
            self.exchanges) + "'" + ',' + "'" + str(self.companies) + "'" + ',' + "'" + encode(
            self.unknown) + "'" + ',' + "'" + str(self.text_type) + "'" + ',' + "'" + encode(
            self.author) + "'" + ',' + "'" + encode(self.dateline) + "'" + ',' + "'" + encode(
            self.title) + "'" + ',' + "'" + encode(self.text_waste) + "'" + ',' + "'" + encode(
            self.body) + "'"


def encode(inp):
    """
    кодирование текста, для записи в бд
    :param inp: текст
    :return: текст, без "запрещённых" символов
    """
    if inp is None or len(inp) == 0:
        return 'None'
    else:
        return str('"/"'.join(inp.split("'")))


def encode_arr(inp):
    """
    кодирование массива, для записи в бд
    :param inp: массив (список)
    :return: строка, закодированная для записи
    """
    if inp is None or len(inp) == 0:
        return 'None'
    else:
        return str('|'.join(inp))


def decode_arr(inp):
    """
    декодирование массива, закодированного encode_arr
    :param inp: кодированный массив
    :return: декодированный массив
    """
    if inp == 'None':
        return list()
    else:
        return inp.split('|')


def decode(inp):
    """
    декодирование текста, закодированного encode
    :param inp: кодированный текст
    :return: декодированный текст
    """
    if inp == 'None':
        return ''
    else:
        return str("'".join(inp.split('"/"')))


def get_collection_categories(adress):
    """
    загрузка имён категорий
    :param adress: адрес директории с расакованным архивом
    :return: список имён категорий
    """
    out = []  # exchanges, orgs, people, places, topics
    filenames = [adress + '/all-exchanges-strings.lc.txt', adress + '/all-orgs-strings.lc.txt',
                 adress + '/all-people-strings.lc.txt', adress + '/all-places-strings.lc.txt',
                 adress + '/all-topics-strings.lc.txt']
    for i in range(len(filenames)):
        f = open(filenames[i], encoding='cp1252')
        out.append(set(map(lambda line: ''.join(''.join(line.split('\n')).split(' ')), f)))
        # 		print(f.split('\n'))
        f.close()
    return out


def loading_text(line, l, body_act, text_act, title_act, obj):
    """
    чтение тектсовых полей
    работает рекурсивно или из open_sgm
    :param line: текст в разметке sgml
    :param l: номер начала тега
    :param body_act: индикатор чтения поля body (bool)
    :param text_act: индикатор чтения поля text (bool)
    :param title_act: индикатор чтения поля body (bool)
    :param obj: объект класса news, поля которого заполняем
    :return: индикаторы (обновлённые body_act, text_act, title_act), обновлённый obj и обновлённый номер начала тега
    """
    if line == '\n':
        return body_act, text_act, title_act, obj, l
    elif line[l:l + 6] == '<BODY>':
        body_act = True  # чтение тела
        obj.set_body(line[l + 6:len(line) - 1])
    elif line[l:l + 7] == '<TITLE>':
        k = skip(l + 9, line, '</TITLE>', '\n')
        obj.set_title(line[l + 7:k])
        if line[k] == '\n':
            obj.set_title('\n')
            title_act = True
        if line[len(line) - 9:len(line) - 1] != '</TITLE>' and not title_act:
            l = skip_unlim(k, line, '<AUTHOR>', '<DATELINE>', '<BODY>', '\n')
            (body_act, text_act, title_act, obj, l) = loading_text(line, l, body_act, text_act, title_act, obj)
    # 		elif title_act:

    elif line[l:l + 8] == '<AUTHOR>':
        k = skip(l + 10, line, '</AUTHOR>')
        obj.set_author(line[l + 8:k])
        if line[len(line) - 10:len(line) - 1] != '</AUTHOR>':
            l = skip_unlim(k, line, '<TITLE>', '<DATELINE>', '<BODY>', '\n')
            (body_act, text_act, title_act, obj, l) = loading_text(line, l, body_act, text_act, title_act, obj)
    elif line[l:l + 10] == '<DATELINE>':
        k = skip(l + 12, line, '</DATELINE>', log=False)
        obj.set_dateline(line[l + 10:k])
        if line[len(line) - 12:len(line) - 1] != '</DATELINE>':
            l = skip_unlim(k, line, '<TITLE>', '<AUTHOR>', '<BODY>', '\n')
            (body_act, text_act, title_act, obj, l) = loading_text(line, l, body_act, text_act, title_act, obj)
    else:
        # 		obj.set_text_waste(line)
        obj.set_text_waste('\n')
        text_act = True
    return body_act, text_act, title_act, obj, l


def open_sgm(filename, array_cat, database=None):
    """
    чтение *.sgm файлов
    :param filename: адрес файла *.sgm (текст)
    :param array_cat: список названий категорий
    :param database: (опционально) адрес бд для выгрузки (текст)
    Если он не задан - выгрузка в бд не происходит
    :return: список объектов типа news, считанных из файла
    """
    f = open(filename, encoding='cp1252')
    if not (database is None):
        try:
            conn = sqlite3.connect(database)
            cursor = conn.cursor()
        except Exception as exceptional:
            print(exceptional)
            database = None
    out = []
    unknown_act = False
    unknown = ''
    body = ''
    body_act = False
    title_act = False
    text_act = False
    first = True  # если это первая строка файла...
    for line in f:
        if first:
            first = False
            if line != '<!DOCTYPE lewis SYSTEM "lewis.dtd">\n':  # ... то проверить на SGML формат
                raise NoSGM
        # первая строка заголовка новости
        elif line[0:8] == '<REUTERS' and not unknown_act and not body_act and not text_act:  # смещение для 1го - 17
            if line[17] == 'Y':  # TOPICS = YES
                k1 = skip(skip(20, line, 'LEWISSPLIT') + 10, line, '"')
                k2 = skip(skip(k1, line, 'CGISPLIT') + 8, line, '"')
                kt = skip(k1, line, 'CSECS', arg2='OLDID')
                if line[kt:kt + 5] == 'CSECS':
                    kt = skip(kt + 5, line, '"')
                    ktend = skip(kt, line, '"')
                    csecs = line[kt:ktend]
                    k3 = skip(skip(kt, line, 'OLDID') + 5, line, '"')
                else:
                    csecs = None
                    k3 = skip(kt + 5, line, '"')
                k4 = skip(skip(k3, line, 'NEWID') + 5, line, '"')
                out.append(news('YES', line[k1 + 1: skip(k1 + 1, line, '"')], line[k2 + 1: skip(k2 + 1, line, '"')],
                                line[k3 + 1: skip(k3 + 1, line, '"')], line[k4 + 1: skip(k4 + 1, line, '"')], csecs))
            elif line[17] == 'N':  # TOPICS = NO
                k1 = skip(skip(19, line, 'LEWISSPLIT') + 10, line, '"')
                k2 = skip(skip(k1, line, 'CGISPLIT') + 8, line, '"')
                kt = skip(k1, line, 'CSECS', arg2='OLDID')
                if line[kt:kt + 5] == 'CSECS':
                    kt = skip(kt + 5, line, '"')
                    ktend = skip(kt + 1, line, '"')
                    csecs = line[kt + 1:ktend]
                    k3 = skip(skip(kt, line, 'OLDID') + 5, line, '"')
                else:
                    csecs = None
                    k3 = skip(kt + 5, line, '"')
                k4 = skip(skip(k3, line, 'NEWID') + 5, line, '"')
                out.append(news('No', line[k1 + 1: skip(k1 + 1, line, '"')], line[k2 + 1: skip(k2 + 1, line, '"')],
                                line[k3 + 1: skip(k3 + 1, line, '"')], line[k4 + 1: skip(k4 + 1, line, '"')], csecs))
            else:  # TOPICS = BYPASS
                k1 = skip(skip(23, line, 'LEWISSPLIT') + 10, line, '"')
                k2 = skip(skip(k1, line, 'CGISPLIT') + 8, line, '"')
                kt = skip(k1, line, 'CSECS', arg2='OLDID')
                if line[kt:kt + 5] == 'CSECS':
                    kt = skip(kt + 5, line, '"')
                    ktend = skip(kt, line, '"')
                    csecs = line[kt:ktend]
                    k3 = skip(skip(kt, line, 'OLDID') + 5, line, '"')
                else:
                    csecs = None
                    k3 = skip(kt + 5, line, '"')
                k4 = skip(skip(k3, line, 'NEWID') + 5, line, '"')
                out.append(news('BYPASS', line[k1 + 1: skip(k1 + 1, line, '"')], line[k2 + 1: skip(k2 + 1, line, '"')],
                                line[k3 + 1: skip(k3 + 1, line, '"')], line[k4 + 1: skip(k4 + 1, line, '"')], csecs))
        elif line[0:6] == '<DATE>' and not unknown_act and not body_act and not text_act:
            # 			out[len(out) - 1].set_date(line[7:skip(7,line,'</DATE>')])
            out[len(out) - 1].set_date(line[6:len(line) - 8])
        elif line[0:8] == '<TOPICS>' and not unknown_act and not (
                body_act) and not text_act:  # в описании сказано, что  TOPICS не сообщает ничего о наличии категорий
            # заголовков, поэтому читаем для всех
            out[len(out) - 1].set_topics((''.join((line[11:len(line) - 14]).split('<D>'))).split('</D>'),
                                         array_cat[4])  # ... и разбиение по </D>, а затем запись в объект
        elif line[0:8] == '<MKNOTE>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_mknote(line[9:skip(7, line, '</MKNOTE>')])
        elif line[0:8] == '<PLACES>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_places((''.join((line[11:len(line) - 14]).split('<D>'))).split('</D>'),
                                         array_cat[3])  # аналогично <TOPICS>
        elif line[0:8] == '<PEOPLE>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_people((''.join((line[11:len(line) - 14]).split('<D>'))).split('</D>'),
                                         array_cat[2])  # аналогично <TOPICS>
        elif line[0:6] == '<ORGS>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_orgs((''.join((line[9:len(line) - 12]).split('<D>'))).split('</D>'),
                                       array_cat[1])  # аналогично <TOPICS>
        elif line[0:11] == '<EXCHANGES>' and not unknown_act and not body_act and not text_act:
            out[len(out) - 1].set_exchanges((''.join((line[14:len(line) - 17]).split('<D>'))).split('</D>'),
                                            array_cat[0])  # аналогично <TOPICS>
        elif line[0:11] == '<COMPANIES>' and not unknown_act and not (
                body_act) and not text_act:  # хотя это излишне: в коллекции нет элементов с информацией под этим
            # тэгом (из описания)
            out[len(out) - 1].set_companies(line[12:len(line) - 12])
        elif line[0:9] == '<UNKNOWN>' and not unknown_act and not body_act and not text_act and not title_act:

            if len(line) > 10 and line[len(line) - 11: len(line) - 1] == '</UNKNOWN>':
                unknown = line[10:len(line) - 11]
            elif len(line) > 10:
                unknown_act = True
                unknown = line[10:len(line) - 1] + '\n'
            else:
                unknown_act = True
        elif unknown_act and not body_act and not text_act:
            if len(line) > 10 and line[len(line) - 11: len(line) - 1] == '</UNKNOWN>':
                unknown += line[0:len(line) - 11]
                out[len(out) - 1].set_unknown(unknown)
                del unknown
                unknown_act = False
            else:
                unknown += line[0:len(line) - 1] + '\n'
        elif line[0:5] == '<TEXT' and not unknown_act and not body_act and not text_act and not title_act:
            if line[5] != '>':
                k = skip(5, line, '"')
                out[len(out) - 1].set_text_type(line[k + 1:skip(k + 1, line, '"')])
                k = skip(k, line, '>')
            else:
                k = 5
            l = skip_unlim(6, line, '<AUTHOR>', '<DATELINE>', '<TITLE>', '<BODY>', '\n')
            out[len(out) - 1].set_text_waste(line[k + 1:l])
            (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act, title_act,
                                                                                 out[len(out) - 1])
        elif line[0:10] == '</REUTERS>':
            if database is not None:
                command = "INSERT into inp values (" + out[len(out) - 1].generate_string() + ") "
                try:
                    cursor.execute(command)
                except sqlite3.DatabaseError as e:
                    print(e)
                    print(command)
                    print('===============================\n==============================')
                else:
                    conn.commit()
            body = ''
            unknown = ''
            unknown_act = False
            body_act = False
            title_act = False
            text_act = False
            continue  # если убрать - метка конца вместе с последующей информацией заносится в waste
        elif text_act and not unknown_act and not body_act and not title_act:
            l = skip_unlim(0, line, '<AUTHOR>', '<DATELINE>', '<TITLE>', '<BODY>', '\n')
            out[len(out) - 1].set_text_waste(line[0:l])
            text_act = False
            (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act, title_act,
                                                                                 out[len(out) - 1])
        elif title_act and not unknown_act and not body_act and not text_act:
            k = skip(0, line, '</TITLE>', '\n')
            if line[k] == '\n':
                out[len(out) - 1].set_title(line)
            else:
                out[len(out) - 1].set_title(line[0:k - 1])
                title_act = False
                l = skip_unlim(k + 8, line, '<AUTHOR>', '<DATELINE>', '<BODY>', '\n')
                out[len(out) - 1].set_text_waste('\n' + line[k + 8:l - 1])
                (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act,
                                                                                     title_act, out[len(out) - 1])
        elif body_act:
            k = skip(0, line, '</BODY>', '\n')
            if line[k] == '\n':
                out[len(out) - 1].set_body(line)
            else:
                out[len(out) - 1].set_body(line[0:k - 1])
                body_act = False
        else:
            (body_act, text_act, title_act, out[len(out) - 1], l) = loading_text(line, l, body_act, text_act, title_act,
                                                                                 out[len(out) - 1])
    # 		out.append(line[0:len(line)-1]) # удаление символа сброса строки
    f.close()
    if database is not None:
        conn.close()
    return out


def decode_from_db(arr, array_cat, cat_num=None):
    """
    декодирование элемента из бд в элемент класса news
    :param arr: декодируемый массив (список)
    :param array_cat: список категорий
    :param cat_num: (опционально) номер категории, по которой генерируется массив для С-шных функций
    (если не указан - этот массив не генерируется)
    :return: список декодированных объектов тиа news и (опционально) массив для фуекций на С
    """
    arr_news = []
    arr_for_c = []
    arr_for_c.append(list())
    arr_for_c.append(list())
    for i in arr:
        arr_news.append(news(i[5], i[2], i[3], i[0], i[1], i[4]))
        arr_news[len(arr_news) - 1].set_date(i[6])
        arr_news[len(arr_news) - 1].set_topics(decode_arr(i[7]), array_cat[4])
        arr_news[len(arr_news) - 1].set_mknote(i[8])
        arr_news[len(arr_news) - 1].set_places(decode_arr(i[9]), array_cat[3])
        arr_news[len(arr_news) - 1].set_people(decode_arr(i[10]), array_cat[2])
        arr_news[len(arr_news) - 1].set_orgs(decode_arr(i[11]), array_cat[1])
        arr_news[len(arr_news) - 1].set_exchanges(decode_arr(i[12]), array_cat[0])
        arr_news[len(arr_news) - 1].set_companies(i[13])
        arr_news[len(arr_news) - 1].set_unknown(decode(i[14]))
        arr_news[len(arr_news) - 1].set_text_type(i[15])
        arr_news[len(arr_news) - 1].set_author(decode(i[16]))
        arr_news[len(arr_news) - 1].set_dateline(decode(i[17]))
        arr_news[len(arr_news) - 1].set_title(decode(i[18]))
        arr_news[len(arr_news) - 1].set_text_waste(decode(i[19]))
        arr_news[len(arr_news) - 1].set_body(decode(i[20]))

        if cat_num is not None:
            if arr_news[len(arr_news) - 1].title is not None and arr_news[len(arr_news) - 1].body is not None:
                arr_for_c[0].append(arr_news[len(arr_news) - 1].title + arr_news[len(arr_news) - 1].body)
            elif arr_news[len(arr_news) - 1].title is not None:
                arr_for_c[0].append(arr_news[len(arr_news) - 1].title)
            elif arr_news[len(arr_news) - 1].body is not None:
                arr_for_c[0].append(arr_news[len(arr_news) - 1].body)
            else:
                arr_for_c[0].append('')

            if cat_num == 0 and len(arr_news[len(arr_news) - 1].exchanges) != 0:
                arr_for_c[1].append('|' + i[12] + '|')
            elif cat_num == 1 and len(arr_news[len(arr_news) - 1].orgs) != 0:
                arr_for_c[1].append('|' + i[11] + '|')
            elif cat_num == 2 and len(arr_news[len(arr_news) - 1].people) != 0:
                arr_for_c[1].append('|' + i[10] + '|')
            elif cat_num == 3 and len(arr_news[len(arr_news) - 1].places) != 0:
                arr_for_c[1].append('|' + i[9] + '|')
            elif cat_num == 4 and len(arr_news[len(arr_news) - 1].topics_array) != 0:
                arr_for_c[1].append('|' + i[7] + '|')
            else:
                arr_for_c[0].append('')
    if cat_num is None:
        return arr_news
    else:
        return arr_news, arr_for_c


def main():
    a = []
    for i in range(10):
        a += open_sgm('reuters21578.tar/reut2-00' + str(i) + '.sgm', get_collection_categories('reuters21578.tar'),
                      'collection.db')

    for i in range(10, 22):
        #		print(i)
        a += open_sgm('reuters21578.tar/reut2-0' + str(i) + '.sgm', get_collection_categories('reuters21578.tar'),
                      'collection.db')
    #	a = open_sgm('reuters21578.tar/reut2-000.sgm', get_collection_categories('reuters21578.tar'), 'collection.db')
    #	for i in a:
    #		i.show()
    # ==============================================
    # создание словаря и поиск самого часто встречающегося слова
    body_dict = dict()
    for text in a:
        if text.body is not None:
            body = text.body.lower().translate(str.maketrans(',:"',
                                                             '   ')).split()  # получить тела, сделать все буквы строчными, заменить лишние символы пробелами и разделить на слова (по стандартному алгоритму)
        if text.title is not None:
            body += text.title.lower().translate(str.maketrans(',:"', '   ')).split()
        for i in body:
            if body_dict.get(i) is None:
                body_dict[i] = 1
            else:
                body_dict[i] += 1
    ans = max(body_dict, key=(lambda key: body_dict[key]))
    print(ans, end=' ')
    print(body_dict[ans])


# ===============================================
# for i in body_dict.keys():
#	print(i)
# print('====================')
# for i in range(len(a)):
#	if a[i].newid != i + 1:
#		print('====================')
#		print(i)
#		a[i].show()
# print('====================')

# for i in a:
#	if i.text_type != 'NORM': 
#		i.show()
# open_sgm('reuters21578.tar/lewis.dtd')
if __name__ == '__main__':
    # main()
    a = open_sgm('reuters21578.tar/reut2-000.sgm', get_collection_categories('reuters21578.tar'))
    print(a[0].generate_string())
