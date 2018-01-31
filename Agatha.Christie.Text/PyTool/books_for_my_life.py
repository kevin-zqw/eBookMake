# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys
from bs4 import BeautifulSoup

if __name__ == '__main__':
    dir_path = '/Users/kevin/Desktop/test'

    for filename in sorted(os.listdir(dir_path)):
        # hidden files
        if not filename.endswith('.xhtml'):
            continue

        file_path = os.path.join(dir_path, filename)
        with open(file_path, 'r', encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

            header = soup.find_all('h2')
            for tag in header:
                author = tag.text.strip()

                next_div_text = tag.findNext("div").text
                book_list = re.findall(r'《.*?》', next_div_text)
                books = ''.join(book_list)

                print(author, books, sep='：')
