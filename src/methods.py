from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import time
import os


main_url = 'http://lib.ru/'
"""
URL pattern: main_url + section_url + author_url + book_url = url
"""
sections = [
    'INOOLD/', 'INPROZ/', 'PROZA/',
    'RUSSLIT/', 'LITRA/', 'PXESY/',
    'NEWPROZA/', 'POEEAST/', 'POECHIN/',
    'TALES/', 'PRIKL/', 'RAZNOE/',
    'SOCFANT/', 'INOFANT/', 'RUFANT/',
    'RUSS_DETEKTIW/', 'FILOSOF/'
]
stop_signal = [False]


def logging(err_msg: str,
            file: str = 'err'):

    with open(file, 'a') as err:
        err.write(f'{err_msg}\n{datetime.now()}\n\n')


def get_page(url,
             n_attempts=1):

    for i in range(n_attempts):
        r = requests.get(url)
        if r.status_code == 200:
            break
        elif r.status_code == 504:
            stop_signal[0] = True
    else:
        logging('error on {0}: status code = {1}'.format(url, r.status_code))
        return None
    return r.text


def good_str(s: str):
    """
        Переписывает строку,
        оствляя ТОЛЬКО буквы,
        и переводит ее в lowercase.

        (некоторые имена могут содержать знак '-',
        который иногда заменяют пробелом,
        поэтому так)
    """
    return ''.join(filter(
        lambda c: c.isalpha(),
        s.lower().replace('ё', 'е')
    ))


def right_tag(tag: BeautifulSoup):
    return tag.name == 'a' and tag.parent.name == 'li'


def create_table_authors(url: str,
                         name: str,
                         and_return: bool = False,
                         save: bool = True):
    """

    :param url: str
        Ссылка на источник.
    :param name:
        Имя создаваемой таблицы
    :param and_return: bool
        Вернуть ли таблицу
    :param save: bool
        Сохранить ли в файл
    """
    page = get_page(url)
    soup = BeautifulSoup(page, "html.parser")
    authors = ((url + a["href"],
                ' '.join(a.text.split())) for i, a in enumerate(soup.find_all(right_tag)))

    df = pd.DataFrame(authors, columns=('url', 'author'))
    if save:
        df.to_csv(f'tables/authors/{name}.csv')
    if and_return:
        return df


def create_all_authors_table(sections: list[str] = sections,
                             main_url: str = main_url):

    tables = []
    for section in sections:
        tables.append(
            create_table_authors(main_url+section, 'None', True, False)
        )
    df = pd.concat(tables, ignore_index=True)
    df.to_csv('tables/authors/lib_ru_authors.csv')


def create_table_books(url: str,
                       table_name: str,
                       author: str,
                       path_to_save: str = 'tables/books/',
                       and_return: bool = False,
                       save: bool = True,
                       waiting_time: float = 1.5):
    """

    :param url: str
        Ссылка на список книг.
    :param table_name:
        Имя создаваемой таблицы.
    :param author:
        ФИО автора.
    :param path_to_save:
        Директория для сохранения.
    :param and_return: bool
        Вернуть ли таблицу.
    :param save: bool
        Сохранить ли в файл.
    :param waiting_time:
        Время сна.
    """
    time.sleep(waiting_time)
    page = get_page(url)
    if page is None:
        logging(f'URL "{url}" is not available. Author: {author}.')
        return None
    soup = BeautifulSoup(page, "html.parser")
    # author = ' '.join(soup.head.title.text.split()[1:])
    books = ((url + a["href"], ' '.join(a.text.split()), author) for a in soup.find_all(right_tag))

    df = pd.DataFrame(books, columns=('url', 'book', 'author'))
    if save:
        df.to_csv(f'{path_to_save}{table_name}.csv')
    if and_return:
        return df


def create_all_tables_books(authors: pd.DataFrame,
                            start_n: int = 0,
                            path_to_save: str = 'tables/books/lib_ru/'):

    for i, row in authors.iterrows():
        if stop_signal[0]:
            break
        url, author = row['url'], row['author']
        if i < start_n:
            continue
        i = str(i).zfill(6)
        create_table_books(url, i, author, path_to_save)


def create_all_books_table(dir_path: str = 'tables/books/lib_ru/',
                           table_name: str = 'original_books.csv',
                           table_path: str = 'tables/books/'):
    names = os.listdir(dir_path)
    tables = []
    for name in names:
        tables.append(
            pd.read_csv(dir_path + name)
        )
    df = pd.concat(tables)
    df.to_csv(table_path+table_name)


"""
Ниже уже не нужные (вроде бы) методы, 
но я боюсь их удалять.
"""


def download_book(url: str, book_name: str = None, path_to_save: str = 'library/'):
    page = get_page(url)
    if page is None:
        return
    soup = BeautifulSoup(page, "html.parser").body.pre.pre
    if book_name is None:
        book_name = str(soup.find('h2').text) + '.txt'
    soup.pre.decompose()
    for tag in soup.find_all(['a', 'b', 'ul', 'h2']):
        tag.unwrap()
    with open(path_to_save + book_name, 'w') as file:
        file.write(soup.text)


def download_books(
        books_for_downloading: pd.DataFrame,
        existing_books: pd.DataFrame,
        path_to_save: str = 'library/'):

    link = existing_books.columns[1]
    for i, row in books_for_downloading.iterrows():
        author, book = row['author'], row['book']
        temp_df = existing_books.loc[(existing_books['author'] == author) & (existing_books['book'] == book)]
        if len(temp_df):
            download_book(link+temp_df.iloc[0][link])
        else:
            logging(f"The book '{book}' by {author} not found.")
