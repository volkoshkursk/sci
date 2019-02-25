import logging


def skip(k, link_text, arg, arg2='!@!', death='!@!', back=False, log=True):
	"""
	поиск в тексте заданного символа, пока не встречен символ остановки
	:param k: номер элемента, с которого начинается поиск
	:param link_text: текст
	:param arg: искомый элемент
	:param arg2: (опционально) искомый элемент (тогда вернётся номер первого встретившегося из arg и arg2)
	:param death: (опционально) элемент, встретив который поиск останавливается. Возвращается длина исходного текста
	:param back: (опционально) поиск в обратную сторону
	:param log: (опционально) логгирование вкл
	:return: номер начала искомого элемента или длина массива, если ничего не найдено
	"""
	while (link_text[k:k+len(arg)] != arg) and (link_text[k:k+len(arg2)] != arg2) and (link_text[k:k+len(death)] != death):
		if k >= len(link_text):
			if log:
				sk_log = logging.getLogger("all_skips.skip")
				sk_log.error("k >= len(link_text)")
				print('error')
			break
		else:
			if not back:
				k += 1
			else:
				k += 1
				if k < 0:
					if log:
						sk_log = logging.getLogger("all_skips.skip")
						sk_log.error("k <= 0")
						print('error')
					break
	if link_text[k:k+len(death)] == death:
		k = len(link_text)
	return k


def skip_unlim(k, link_text, log=True, *args):
	"""
	поиск в тексте заданных символов
	:param k: номер элемента, с которого начинается поиск
	:param link_text: текст
	:param log: (опционально) логгирование вкл
	количество искомых элементов не ограничено
	:return: номер начала искомого элемента или длина массива, если ничего не найдено
	"""
	cond = link_text[k:k+len(args[0])] != args[0]
	for i in range(len(args)):
		cond = cond and link_text[k:k+len(args[i])] != args[i]
	while cond:
		if k > len(link_text):
			if log:
				sk_log = logging.getLogger("all_skips.skip_unlim")
				sk_log.error("k > len(link_text)")
				print('error')
			break
		elif k == len(link_text):
			return k
		else:
			k += 1
			for i in range(len(args)):
				cond = cond and link_text[k:k+len(args[i])] != args[i]
	return k


def skip_s(k, link_text, arg, arg2='!@!', death='!@!'):
	"""
	поиск в тексте заданного символа, пока не встречен символ остановки
	от skip отличается тем, что возвращает позицию, на которой остановился
	:param k: номер элемента, с которого начинается поиск
	:param link_text: текст
	:param arg: искомый элемент
	:param arg2: (опционально) искомый элемент (тогда вернётся номер первого встретившегося из arg и arg2)
	:param death: (опционально) элемент, встретив который поиск останавливается. Возвращается длина исходного текста
	:return: позицию, на которой поиск остановился
	"""
	while not (not (link_text[k:k + len(arg)] != arg) or not (link_text[k:k + len(arg2)] != arg2) or not (
			link_text[k:k + len(death)] != death)):
		if k >= len(link_text):
			sk_log = logging.getLogger("all_skips.skip_s")
			sk_log.error("k >= len(link_text)")
			print('error')
			break
		else:
			k += 1
	return k


def skip_not(k, link_text, arg, arg2='!@!'):
	"""
	поиск конца заданной последовательности элементов
	:param k: номер элемента, с которого начинается поиск
	:param link_text: текст
	:param arg: элемент, конец которого ищем
	:param arg2: (опционально) элемент, конец которого ищем
	:return: 2-й элемент последнего элемента arg/arg2
	"""
	while (link_text[k:k+len(arg)] == arg) or (link_text[k:k+len(arg2)] == arg2):

		if k >= len(link_text):
			sk_log = logging.getLogger("all_skips.skip_not")
			sk_log.error("k >= len(link_text)")
			print('error')
			break
		k += 1
	return k


def skip_to_int(k, link_text, another={0}):  # another - это множество
	"""
	поиск числа или символа из множества
	:param k: номер элемента, с которого начинается поиск
	:param link_text: текст
	:param another:  (опционально) (set)
	:return: номер первого числа/элемента из another
	"""
	try:
		int(link_text[k])
	except Exception as E:
		t = True
	else:
		t = False
	if k < len(link_text):
		an = not(link_text[k] in another)
	else:
		an = False
	while k < len(link_text) and (t and an):
		try:
			int(link_text[k])
		except Exception as E:
			t = True
		else:
			t = False
		an = not(link_text[k] in another)
		if t and an:
			k += 1
	return k


def skip_while_int(k, link_text, another={0}):  # another - это множество
	"""
	поиск конца последовательности чисел или символов из множества
	:param k: номер элемента, с которого начинается поиск
	:param link_text: текст
	:param another: (опционально)(set)
	:return: номер первого элемента не из множества чисел/элементов из another
	"""
	try:
		int(link_text[k])
	except Exception as E:
		t = False
	else:
		t = True

	if k < len(link_text):
		an = link_text[k] in another
	else:
		an = False
	while k < len(link_text) and (t or an):
		try:
			int(link_text[k])
		except Exception as E:
			t = False
			an = link_text[k] in another
			if an:
				k += 1
		else:
			t = True
			k += 1
	return k


def skip_while(k, link_text, another):
	while k < len(link_text) and (link_text[k] in another):
			k += 1
	return k
