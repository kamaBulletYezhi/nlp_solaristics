from bs4 import BeautifulSoup
import requests
import pandas as pd


main_url = 'http://lib.ru/'
"""
URL pattern: main_url + section_url + author_url + book_url = url
"""


def get_page(url, n_attempts=5):
    for i in range(n_attempts):
        r = requests.get(url)
        if r.status_code == 200:
            break
    else:
        print('error on {0}: status code = {1}'.format(url, r.status_code))
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
    authors = ((a["href"], ' '.join(a.text.split())) for a in soup.find_all(right_tag))

    df = pd.DataFrame(authors, columns=(url, 'author'))
    if save:
        df.to_csv(f'tables/authors/{name}.csv')
    if and_return:
        return df


def create_table_books(url: str, name: str, and_return: bool = False, save: bool = True):
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
    author = ' '.join(soup.head.title.text.split()[1:])
    books = ((a["href"], ' '.join(a.text.split()), author) for a in soup.find_all(right_tag))

    df = pd.DataFrame(books, columns=(url, 'book', 'author'))
    if save:
        df.to_csv(f'tables/books/{name}.csv')
    if and_return:
        return df


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


def download_all_books(path: str):
    df = pd.read_csv(path)
    link = df.columns[1]
    for i, row in df.iterrows():
        download_book(link+row[1], f'test_{i:03d}.txt')


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
            print(f"The book '{book}' by {author} not found.")










if __name__ == "__main__":
    # temp_url = "http://www.lib.ru/INOOLD/DUMA/tri.txt"
    # duma = "http://www.lib.ru/INOOLD/DUMA/"
    # create_table_books(duma, 'DUMA')
    #create_table_authors('http://lib.ru/INOOLD/', 'INOOLD')
    pass



