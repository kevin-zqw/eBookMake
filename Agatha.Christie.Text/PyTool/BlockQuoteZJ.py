# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


def process_block_quote(file_path):
    search_text = 'bodycontent-text_yinwen'
    start_tag = '<blockquote>\n'
    end_tag = '</blockquote>\n'

    with open(file_path, 'r+', encoding='utf-8') as f:
        result_lines = []
        block_started = False

        for line in f.readlines():
            if search_text in line and not block_started:
                result_lines.append(start_tag)
                result_lines.append(line)
                block_started = True
                continue

            if search_text not in line and block_started:
                result_lines.append(end_tag)
                result_lines.append(line)
                block_started = False
                continue

            result_lines.append(line)

        f.seek(0)
        f.write(''.join(result_lines))
        f.truncate()


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        dir_path = sys.argv[1]
        for filename in os.listdir(dir_path):
            if not filename.endswith('.xhtml'):
                continue

            file_path = os.path.join(dir_path, filename)
            process_block_quote(file_path)
