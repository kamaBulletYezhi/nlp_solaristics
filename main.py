from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import src.methods as methods


main_url = 'http://lib.ru/'
sections = [
    'INOOLD/', 'INPROZ/', 'PROZA/',
    'RUSSLIT/', 'LITRA/', 'PXESY/',
    'NEWPROZA/', 'POEEAST/', 'POECHIN/',
    'TALES/', 'PRIKL/', 'RAZNOE/',
    'SOCFANT/', 'INOFANT/', 'RUFANT/',
    'RUSS_DETEKTIW/', 'FILOSOF/'
]

if __name__ == "__main__":
    path = 'tables/authors/lib_ru_authors.csv'
    df = pd.read_csv(path)
    #methods.create_all_authors_table(sections, main_url)
    methods.create_all_tables_books(df, 422) # 854



