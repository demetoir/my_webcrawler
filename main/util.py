import shutil
import os
import webbrowser

from main.DbContract import *


def clean_up():
    if os.path.exists(DBContract.DB_PATH):
        shutil.rmtree(DBContract.DB_PATH)


def print_rows(rows):
    print('total = %d' % len(rows))
    for row in rows:
        print(row)
    print()


def print_parse_items(items):
    for item in items:
        print(item)


def print_soup_children(soup):
    for i, child in enumerate(soup.children):
        if child.name is None:
            continue
        print(i, child.name, child.attrs)
    print()


def open_web(html):
    # write html file
    path = os.path.curdir
    file_name = 'punning_html.html'
    full_path = os.path.join(path, file_name)
    with open(full_path, 'wb') as f:
        f.write(html.encode('utf-8'))

    webbrowser.open_new_tab(full_path)


if __name__ == '__main__':
    clean_up()
