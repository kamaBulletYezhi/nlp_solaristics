from bs4 import BeautifulSoup as BS
import requests
import pandas as pd
import src.methods as methods


main_url = 'http://lib.ru/'
sections = [
    'INOOLD/',
    'INPROZ/',
    'PROZA/'  # и еще что то, потом допишу, парсить нет смысла )))))))))
]

if __name__ == "__main__":
    path = 'tables/authors/PROZA.csv'
    df = pd.read_csv(path)
    #methods.create_table_books_from_table_authors(df, 'ALLPROZA')
    #methods.create_table_authors(main_url+sections[2], sections[2][:-1])
    #methods.create_table_books(main_url+sections[2], sections[2][:-1])
    #methods.download_books(df, df)
    #methods.download_all_books(path)
    # temp_url = "http://www.lib.ru/INOOLD/DUMA/tri.txt"
    #duma = "http://www.lib.ru/INOOLD/DUMA/"
    #methods.create_table_books(duma, 'DUMA')
    # methods.create_table_authors('http://lib.ru/INOOLD/', 'INOOLD')

