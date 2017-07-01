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


def append_header(all_text, header):
    all_text.append(h1_tag + header)
    all_text.append(new_line)


def append_section_header(all_text, header):
    h2 = h2_tag + header
    if h2 not in all_text:
        all_text.append(h2)


def process_sub_dir(dir_path):
    all_text = []

    zh_file = os.path.join(dir_path, 'zh')
    if not os.path.exists(zh_file):
        print('zh file not found!!!')
        return

    with open(zh_file, 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        header = soup.find('h2').text.strip()
        append_header(all_text, header)

        for tag in soup.find_all('a', class_='nourl'):
            href = tag['href']
            sec_name = re.sub(r'taiping-guangji/\d+/', '', href)
            sec_name = re.sub(r'/zh', '', sec_name)

            sec_path = os.path.join(dir_path, sec_name)
            textArray = process_html(sec_path, True)
            all_text.extend(textArray)

    save_file(all_text)


def process_html(html_path, is_sub_file):
    if not os.path.exists(html_path):
        print(html_path, 'not found!!!')
        return []

    print(html_path)

    all_text = []
    with open(html_path, 'r', encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

        all_header = []
        for tag in soup.find_all('h2'):
            all_header.append(tag.text.strip())

        all_contents = []
        is_start = True
        left = ''
        for tag in soup.find_all('td', class_='ctext'):
            for span in tag.findChildren('span', class_='inlinecomment1'):
                span.replace_with(comment_start + span.text + comment_end)

            if is_start:
                left = tag.text.strip()
            else:
                right = tag.text.strip()
                all_contents.append((left, right))

            is_start = not is_start

        if is_sub_file:
            if len(all_header) > 0:
                append_section_header(all_text, all_header[0])
        else:
            if len(all_header) > 0:
                append_header(all_text, all_header[0])

        cache = []
        head_index = 1
        for (left, right) in all_contents:
            if (not is_sub_file) and (len(left) > 0) and (left not in cache):
                cache.append(left)

                if head_index < len(all_header):
                    append_section_header(all_text, all_header[head_index])
                    head_index += 1

            all_text.append(right)
            all_text.append(new_line)
    return all_text


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

        if os.path.isfile(file_path):
            textArray = process_html(file_path, False)
            save_file(textArray)
        else:
            process_sub_dir(file_path)
