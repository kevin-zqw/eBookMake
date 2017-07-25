# -*- coding: utf-8 -*-
__author__ = 'kevin'

from bs4 import BeautifulSoup
import os
import re


base_dir = '/Users/kevin/GitHub/eBookMake/zuihoudediqiuzhanshen'
dest_dir = os.path.join(base_dir, 'output')
separator = 'AAAAAABBBBBB'


def process_file(filename):
    print(filename)

    file_path = os.path.join(base_dir, filename)
    output_name = os.path.splitext(filename)[0] + '.txt'

    with open(file_path, 'r', encoding='utf-8') as f:
        all_text = []
        soup = BeautifulSoup(f, "html.parser")
        h1 = soup.find('h1')
        all_text.append(h1.text.strip())

        tag = soup.find('div', id='content')
        content = tag.text.strip()

        array = content.split(separator)
        for (i, line) in enumerate(array):
            line = line.strip()

            if i == 0 and line.replace(' ', '') == all_text[0].replace(' ', ''):
                print(line)
                continue

            all_text.append(line)





if __name__ == '__main__':

    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    for filename in os.listdir(base_dir):
        if not filename.startswith('part_'):
            continue

        process_file(filename)
