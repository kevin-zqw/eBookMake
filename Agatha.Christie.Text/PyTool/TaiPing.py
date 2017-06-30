# -*- coding: utf-8 -*-
__author__ = 'kevin'

from bs4 import BeautifulSoup
import os
import re


dest_dir = r'/Users/kevin/Desktop/TaiPingGuangJi'


def process_tof(path, name):
    all_text = []

    with open(os.path.join(path, name), 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        for tag in soup.find_all('a', class_='nourl'):
            href = tag['href']
            href = re.sub(r'taiping-guangji/\d+/', '', href)
            href = re.sub(r'/zh', '', href)
            all_text.append(tag.text + ' ' + href)

    save_file(all_text, path, name)


def process_html(path, name):
    all_text = []

    with open(os.path.join(path, name), 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        for tag in soup.find_all('h2'):
            all_text.append(tag.text.strip())

        is_start = True
        line = ''
        for tag in soup.find_all('td', class_='ctext'):
            if is_start:
                line = tag.text.strip()
            else:
                line += tag.text.strip()
                all_text.append(line)

            is_start = not is_start

    save_file(all_text, path, name)


def save_file(all_text, path, name):
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    dir_name = os.path.basename(path)

    file_path = ''
    if dir_name == 'taiping-guangji':
        filename = name.zfill(3) + '.txt'
        file_path = os.path.join(dest_dir, filename)
    else:
        dir_path = os.path.join(dest_dir, dir_name)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        filename = 's' + dir_name.zfill(3) + '_' + name + '.txt'
        file_path = os.path.join(dir_path, filename)

    with open(file_path, 'w', encoding="utf-8") as file:
        file.write('\n'.join(all_text))


if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookMake/taipinguangji/ctext.org/taiping-guangji'

    for path, subdirs, files in os.walk(base_dir):
        for name in files:
            if name == '.DS_Store':
                continue

            print(path, name)
            if name == 'zh':
                process_tof(path, name)
            else:
                process_html(path, name)

