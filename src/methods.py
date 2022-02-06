from bs4 import BeautifulSoup
from datetime import datetime
import requests
import pandas as pd
import time



main_url = 'http://lib.ru/'
"""
URL pattern: main_url + section_url + author_url + book_url = url
"""


def logging(err_msg: str, file: str = 'err'):
    with open(file, 'a') as err:
        err.write(f'{err_msg}\n{datetime.now()}\n\n')


def get_page(url, n_attempts=1):
    for i in range(n_attempts):
        r = requests.get(url)
        if r.status_code == 200:
            break
    else:
        logging('error on {0}: status code = {1}'.format(url, r.status_code))
        return None
    return r.text


def right_tag(tag: BeautifulSoup):
    return tag.name == 'a' and tag.parent.name == 'li'


def create_table_authors(url: str, name: str, and_return: bool = False, save: bool = True):
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
    authors = ((url + a["href"], ' '.join(a.text.split()), str(i).zfill(6)) for i, a in enumerate(soup.find_all(right_tag)))

    df = pd.DataFrame(authors, columns=('url', 'author', 'id'))
    if save:
        df.to_csv(f'tables/authors/{name}.csv')
    if and_return:
        return df


def create_all_authors_table(sections: list[str], main_url: str = main_url):
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
                       save: bool = True, waiting_time: float = 1.):
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


def create_all_tables_books(authors: pd.DataFrame, path_to_save: str = 'tables/books/lib_ru/'):
    for i, row in authors.iterrows():
        url, author, id = row['url'], row['author'], row['id']
        id = str(id).zfill(6)
        create_table_books(url, id, author, path_to_save)


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
        # book_name = row['file']
        temp_df = existing_books.loc[(existing_books['author'] == author) & (existing_books['book'] == book)]
        if len(temp_df):
            download_book(link+temp_df.iloc[0][link])
        else:
            logging(f"The book '{book}' by {author} not found.")


if __name__ == "__main__":
    # temp_url = "http://www.lib.ru/INOOLD/DUMA/tri.txt"
    # duma = "http://www.lib.ru/INOOLD/DUMA/"
    # create_table_books(duma, 'DUMA')
    #create_table_authors('http://lib.ru/INOOLD/', 'INOOLD')
    pass



