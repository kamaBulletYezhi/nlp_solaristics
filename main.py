import pandas as pd
import src.methods as methods


if __name__ == "__main__":
    path = 'tables/books/original_books.csv' # тута все книги для скачивания
    df = pd.read_csv(path)
    print(len(df)) # 19_718
    #methods.create_all_authors_table(sections, main_url)
    #methods.create_all_tables_books(df)

    # когда будут все таблы надо их склеить в одну
    #methods.create_all_books_table()



