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
            matches = re.findall(r'[，。？！—、：<；>]\d{1,2}[^，。？！—、’”：<；>]', line)
            if len(matches) == 0:
                result_lines.append(line + new_line)
            else:
                if line.startswith('<p>1'):
                    result_lines.append(line + new_line)
                else:
                    pre_line = result_lines[-1].strip()
                    result_lines[-1] = pre_line.replace('</p>', '') + line.replace('<p>', '') + new_line

        file.seek(0)
        file.write(''.join(result_lines))
        file.truncate()


if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookMake/MaoDunWenXueJiang/test'
    for filename in os.listdir(base_dir):
        if not filename.endswith('.xhtml'):
            continue

        file_path = os.path.join(base_dir, filename)
        check_error(file_path)
