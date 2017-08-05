# -*- coding: utf-8 -*-
__author__ = 'kevin'

from bs4 import BeautifulSoup
import os
import shutil
import re
import sys


if __name__ == '__main__':
    toc_dir = r'/Users/kevin/GitHub/eBookMake/LaoSheQuanJi/index/toc/'
    txt_file = '/Users/kevin/GitHub/eBookMake/LaoSheQuanJi/index/index.txt'

    all_entries = []
    for filename in os.listdir(toc_dir):
        file_path = os.path.join(toc_dir, filename)

        with open(file_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            for tag in soup.find_all('a'):
                all_entries.append([tag.text.strip(), tag['href']])

    with open(txt_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line) == 0:
                continue
            
            found = False
            href_array = []
            for toc_pair in all_entries:
                if line == toc_pair[0]:
                    href_array.append(toc_pair[1])
                    found = True
            
            if found:
                print('[match]:', line, ':', href_array)
                
            if not found:
                for toc_pair in all_entries:
                    if toc_pair[0] in line:
                        href_array.append(toc_pair[1])
                        found = True
                
                if found:
                    print('[maybe]:', line, ':', href_array)
                    
            if not found:
                print('[Not]:', line)

