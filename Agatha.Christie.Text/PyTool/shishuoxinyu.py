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


def process_comment(path, replace):
    print(os.path.basename(path))

    all_text = ''
    with open(path, 'r', encoding='utf-8') as file:
        all_text = file.read()

    all_comments = re.findall(r'(<p class="fnote"><a id=".*?" href=".*?">(\(.*?\))</a>(.*?)</p>)', all_text)
    if len(all_comments) == 0:
        return

    start_index = 0
    end_index = 0
    insert_index = 1
    for i, (comm_text, comm_key, comm_value) in enumerate(all_comments):
        if not replace and comm_key == '(1)':
            start_index = end_index
            end_index = all_text.find(comm_text)
        all_text = all_text.replace(comm_text, '')

        escape_key = comm_key.replace('(', r'\(')
        escape_key = escape_key.replace(')', r'\)')
        pattern_replace = r'<a id="[\w\d\-]*?" href="[\./\w\d#\-]*?"><sup>{}</sup></a>'.format(escape_key)
        if replace:
            repl_replace = r'【【{}||{}】】'.format(insert_index, comm_value)
            insert_index += 1
            all_text = re.sub(pattern_replace, repl_replace, all_text, 1)
        else:
            search_text = all_text[start_index:end_index]
            inserts = re.findall(pattern_replace, search_text)
            if len(inserts) != 1:
                print(comm_key, comm_value)
    if replace:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(all_text)


if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookMake/MaoDunWenXueJiang/test'
    for filename in os.listdir(base_dir):
        if not filename.endswith('.xhtml'):
            continue

        file_path = os.path.join(base_dir, filename)
        process_comment(file_path, True)
