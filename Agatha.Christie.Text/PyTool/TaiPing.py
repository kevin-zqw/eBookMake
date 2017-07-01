# -*- coding: utf-8 -*-
__author__ = 'kevin'

from bs4 import BeautifulSoup
import os
import re


base_dir = r'/Users/kevin/GitHub/eBookMake/taipinguangji/ctext.org/taiping-guangji'
output_file = r'/Users/kevin/Desktop/TaiPingGuangJi.txt'

h1_tag = r'#####'
h2_tag = r'&&&&&'
comment_start = r'【【'
comment_end = r'】】'
new_line = '\n'
triple_new_line = '\n\n\n'


def process_sub_dir(dir_path):
    all_text = []

    zh_file = os.path.join(dir_path, 'zh')
    print(zh_file)

    with open(zh_file, 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        for tag in soup.find_all('a', class_='nourl'):
            href = tag['href']
            href = re.sub(r'taiping-guangji/\d+/', '', href)
            href = re.sub(r'/zh', '', href)
            all_text.append(tag.text + ' ' + href)


def process_single_html(html_path):
    all_text = []
    with open(html_path, 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        header = soup.find('h2').text.strip()
        all_text.append(h1_tag + header)
        all_text.append(new_line)

        is_start = True
        left = ''
        right = ''
        for tag in soup.find_all('td', class_='ctext'):
            for span in tag.findChildren('span', class_='inlinecomment1'):
                span.replace_with(comment_start + span.text + comment_end)

            if is_start:
                left = tag.text.strip().replace(':', '')
                left = left.replace('：', '')
            else:
                right = tag.text.strip()

                h2 = h2_tag + '《' + left + '》'
                if h2 not in all_text:
                    all_text.append(h2)

                all_text.append(right)
                all_text.append(new_line)

            is_start = not is_start
    save_file(all_text)


def save_file(all_text):
    with open(output_file, 'a', encoding="utf-8") as file:
        file.write(new_line.join(all_text))
        file.write(triple_new_line)


if __name__ == '__main__':
    if os.path.exists(output_file):
        os.remove(output_file)

    for filename in os.listdir(base_dir):
        if filename == '.DS_Store':
            continue

        file_path = os.path.join(base_dir, filename)
        print(file_path)

        if os.path.isfile(file_path):
            process_single_html(file_path)
        else:
            process_sub_dir(file_path)
