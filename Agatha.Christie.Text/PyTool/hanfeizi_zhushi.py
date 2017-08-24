# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


new_line = '\n'


def check_error(path):
    with open(path, 'r+', encoding='utf-8') as file:
        all_line = file.readlines()
        body_found = False
        result_lines = []
        for i, line in enumerate(all_line):
            if line.strip() == '<body>':
                body_found = True
            if line.strip() == '</body>':
                body_found = False

            if not body_found:
                result_lines.append(line)
                continue

            line = line.strip()
            matches = re.findall(r'[，。？！—、：<；>]\d{1,2}[，。？！—、：<；>]', line)
            if len(matches) == 0:
                result_lines.append(line + new_line)
            else:
                if line.startswith('<p>1'):
                    result_lines.append(line + new_line)
                else:
                    print(line)
                    pre_line = result_lines[-1].strip()
                    result_lines[-1] = pre_line.replace('</p>', '') + line.replace('<p>', '') + new_line

        file.seek(0)
        file.write(''.join(result_lines))
        file.truncate()


def process_comment(path):
    print(os.path.basename(path))

    all_text = ''
    with open(path, 'r', encoding='utf-8') as file:
        all_text = file.read()

    all_comments = re.findall(r'<p>1(.*?)</p>', all_text)
    if len(all_comments) == 0:
        return

    for comment in all_comments:
        all_text = all_text.replace('<p>{}</p>'.format(comment), '')

        pair_array = []
        last_index = 0
        comment_key = '1'
        for match in re.finditer(r'[，。？！—、：<；>’”](\d{1,2})[^\d]', comment):
            comment_value = comment[last_index:match.start()+1]
            # print(comment_key, '=>', comment_value)
            pair_array.append((comment_key, comment_value))

            last_index = match.end()-1
            comment_key = match.group(1)

        # add the last comment
        # print(comment_key, '=>', comment[last_index:])
        pair_array.append((comment_key, comment[last_index:]))

        index = 0
        for key, value in pair_array:
            curr_index = int(key)
            if curr_index != index + 1:
                print(key, '=>', value)
            index = curr_index


if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookMake/MaoDunWenXueJiang/test'
    for filename in os.listdir(base_dir):
        if not filename.endswith('.xhtml'):
            continue

        file_path = os.path.join(base_dir, filename)
        process_comment(file_path)
