import numpy as np
from base import *

matrix = np.loadtxt('lambda')

# TODO make it in function

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

