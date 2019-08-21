from _lda import *
import progressbar
import argparse
"""
Вспомогательные операции: разбиение коллекции на тестовое и обучающее и тд
"""


def train_test_split(path, non_marked=False):
    conn = sqlite3.connect(path)
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor = conn.cursor()
    num = 4
    cat = get_collection_categories('reuters21578.tar')
    cursor.execute("select * from all_data where all_data." + groupname[num] + "!= 'None'")
    inp = decode_from_db(cursor.fetchall(), cat)
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(inp)).start()
    for i in range(len(inp)):
        bar.update(i)
        if i % 10 == 0:
            cursor.execute("INSERT into test values (" + inp[i].generate_string() + ")")
            # conn.commit()
        else:
            cursor.execute("INSERT into inp values (" + inp[i].generate_string() + ")")
        conn.commit()
    bar.finish()
    if non_marked:
        del inp
        cursor.execute("select * from all_data where all_data." + groupname[num] + "== 'None'")
        inp = decode_from_db(cursor.fetchall(), cat)
        bar = progressbar.ProgressBar(widgets=widgets, max_value=len(inp)).start()
        for i in range(len(inp)):
            cursor.execute("INSERT into inp values (" + inp[i].generate_string() + ")")

            bar.update(i)
        conn.commit()
        bar.finish()
    conn.close()


def most_popular_cat(path, count, output, non_marked=False):
    if output is None:
        raise RuntimeError('No output database selected')
    conn_in = sqlite3.connect(path)
    conn_out = sqlite3.connect(output)
    cursor_out = conn_out.cursor()
    groupname = ['exchanges', 'orgs', 'people', 'places', 'topics_array']
    cursor_in = conn_in.cursor()
    num = 4
    cat = get_collection_categories('reuters21578.tar')
    if non_marked:
        cursor_in.execute("select * from all_data")
    else:
        cursor_in.execute("select * from all_data where all_data." + groupname[num] + "!= 'None'")
    inp = decode_from_db(cursor_in.fetchall(), cat)
    conn_in.close()
    widgets = [progressbar.Percentage(), progressbar.Bar()]
    bar = progressbar.ProgressBar(widgets=widgets, max_value=len(inp)).start()
    themes = {i[0] for i in sorted(sort_docs(cat[num], inp).items(), key=lambda kv: -len(kv[1]))[:count]}
    for i in range(len(inp)):
        bar.update(i)
        if len(set(inp[i].topics_array).intersection(themes)) > 0:
            cursor_out.execute("INSERT into all_data values (" + inp[i].generate_string() + ")")
        elif len(inp[i].topics_array) == 0:
            cursor_out.execute("INSERT into all_data values (" + inp[i].generate_string() + ")")
    conn_out.commit()
    conn_out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='tts - train test split \n mpc - most popular categories')
    parser.add_argument('type', choices=['tts', 'mpc', 'scissors'], help='Mode')
    parser.add_argument('path', type=str, help='Path to db')
    parser.add_argument(
        '-nm',
        '--non_marked',
        type=bool,
        default=False,
        help='add non marked (default: False)'
    )
    parser.add_argument(
        '-c',
        '--count',
        type=int,
        default=10,
        help='how much most popular category need'
    )
    parser.add_argument(
        '-dbn',
        '--database_name',
        type=str,
        default=None,
        help='Name of output database (for mpc)'
    )
    arg = parser.parse_args()
    if arg.type == 'tts':
        train_test_split(arg.path, arg.non_marked)
    elif arg.type == 'mpc':
        print(arg)
        most_popular_cat(arg.path, arg.count, arg.database_name, arg.non_marked)
