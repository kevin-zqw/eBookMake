# -*- coding: utf-8 -*-
__author__ = 'kevin'

from bs4 import BeautifulSoup
import os
import re


if __name__ == '__main__':
    base_dir = '/Users/kevin/GitHub/eBookMake/zuihoudediqiuzhanshen'
    index_path = os.path.join(base_dir, 'index.html')

    with open(index_path, 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        file_index = 1
        for tag in soup.find_all('dd'):
            a = tag.find('a')
            href = a['href']
            
            new_name = 'part_' + str(file_index).zfill(4) + '.xhtml'
            file_index += 1

            src_path = os.path.join(base_dir, href)
            dest_path = os.path.join(base_dir, new_name)

            os.rename(src_path, dest_path)
