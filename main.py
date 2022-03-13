import pandas as pd
import src.books_methods as books_methods
import src.summaries_methods as summaries_methods
import time
from random import random


if __name__ == "__main__":
    path = "library/"
    df_merged = pd.read_csv("tables/good_merged.csv")
    for row in df_merged.iloc:
        if row["id"] < 60:
            continue
        file_id = str(row["id"]).zfill(4)
        book_url = row["url_x"]
        summary_url = row["url_y"]

        ok = books_methods.download_book(book_url, file_id)
        if ok:
            summaries_methods.write_summary_from_link(summary_url, file_id)
        time.sleep(2+random())




