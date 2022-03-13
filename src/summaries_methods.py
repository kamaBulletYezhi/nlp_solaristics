from bs4 import BeautifulSoup
import requests
import pandas as pd

briefly_url = 'https://briefly.ru'


def get_page(url):
    for i in range(5):
        r = requests.get(url)
        if r.status_code == 200:
            break

    if r.status_code != 200:
        print('error on {0}: status code = {1}'.format(url, r.status_code))

    return r.text


def get_authors_links():
    authors_url = 'https://briefly.ru/authors/'
    soup = BeautifulSoup(get_page(authors_url), 'lxml')

    authors = soup.find_all('div', class_='letter')[4]  # на Д

    links = authors.find_all('a')
    links = map(lambda tag: tag['href'], links)
    links = filter(lambda link: not link.startswith('/surnames/'), links)
    links = map(lambda link: briefly_url + link, links)

    return list(links)


def get_summaries_links(author_url):
    soup = BeautifulSoup(get_page(author_url), 'lxml')

    author_name = soup.find('span', class_="author_name long")
    if author_name == None:
        author_name = soup.find('span', class_="author_name normal")

    author_name = author_name.text

    summaries_block = soup.find('section', class_='works_index')

    if summaries_block == None:
        return author_name, []

    links = summaries_block.find_all('a')
    links = map(lambda tag: tag['href'], links)
    links = filter(lambda link: link[0] == '/', links)
    links = map(lambda link: briefly_url + link, links)

    return author_name, list(links)


def get_summary(summary_url):
    soup = BeautifulSoup(get_page(summary_url), 'lxml')

    book_name = soup.find('span', class_="main").text

    full = soup.find('div', id='text')
    text_blocks = full.find_all('p')
    text_blocks = map(lambda tag: tag.text, text_blocks)

    text_blocks = map(lambda text: text.replace(u'\xa0', u' '), text_blocks)
    text_blocks = map(lambda text: text.replace(u'\u2009', u' '), text_blocks)

    return book_name, list(text_blocks)


def write_summary(file_id, summary):
    path = 'library/summaries/' + str(file_id) + '.txt'
    with open(path, 'w') as f:
        for block in summary:
            f.write(block)
            f.write('\n')


def write_summary_from_link(summary_url, file_id):
    _, summary = get_summary(summary_url)
    write_summary(file_id, summary)
