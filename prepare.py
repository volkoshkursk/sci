from base import *

"""
модуль для создания файла словаря
"""

conn = sqlite3.connect('collection_full.db')
groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
cursor = conn.cursor()

num = 4

cat = get_collection_categories('reuters21578.tar')

cursor.execute("select word,mi from " + groupname[num] + " where 1=1 order by mi desc")
ans = cursor.fetchall()

f = open('dictionary', 'w')
f.write('\n'.join([i[0] for i in ans]))
f.close()
