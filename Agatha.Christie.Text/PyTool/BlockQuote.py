# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


def process_block_quote(file_path):
    custom_start = 'bbb'
    custom_end = 'ccc'
    start_tag = '<blockquote>'
    end_tag = '</blockquote>'
    with open(file_path, 'r+', encoding='utf-8') as f:
        result_lines = []
        block_started = False
        for line in f.readlines():
            is_block_tag = False
            if custom_start in line or start_tag in line:
                block_started = True
                is_block_tag = True
            if custom_end in line or end_tag in line:
                block_started = False
                is_block_tag = True

            if block_started and not is_block_tag:
                trimmed = line.strip()
                line = '<p>{}</p>\n'.format(trimmed)

            if is_block_tag:
                line = line.replace(custom_start, start_tag)
                line = line.replace(custom_end, end_tag)

            result_lines.append(line)


        f.seek(0)
        f.write(''.join(result_lines))
        f.truncate()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        file_path = sys.argv[1]
        process_block_quote(file_path)
