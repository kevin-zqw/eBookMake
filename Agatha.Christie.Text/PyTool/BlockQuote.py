# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


def process_block_quote(file_path):
    with open(file_path, 'r+', encoding='utf-8') as f:
        result_lines = []
        block_started = False
        for line in f.readlines():
            need_process = True
            if 'bbb' in line or '<blockquote>' in line:
                block_started = True
                need_process = False
            if 'ccc' in line or '</blockquote>' in line:
                block_started = False
                need_process = False

            if need_process and block_started:
                trimmed = line.strip()
                line = '<p>{}</p>\n'.format(trimmed)

            result_lines.append(line)


        f.seek(0)
        f.write(''.join(result_lines))
        f.truncate()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
        process_block_quote(file_path)
