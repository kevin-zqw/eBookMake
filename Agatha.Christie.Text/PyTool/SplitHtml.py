# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


if __name__ == '__main__':
    # command line parameters
    if len(sys.argv) < 5:
        print('python SplitHtml.py <src_file> <template_file> <output_dir> <name_prefix>')
        exit(1)

    src_file = sys.argv[1]
    template_file = sys.argv[2]
    output_dir = sys.argv[3]
    name_prefix = sys.argv[4]

    # constants
    padding = '  '
    mark_break = 'break'
    blockquote_start = '<blockquote>'
    blockquote_end = '</blockquote>'

    # TODO: check command line

    if not os.path.exists(src_file) or not os.path.isfile(src_file):
        print('Source file error')
        exit(0)

    if not os.path.exists(template_file) or not os.path.isfile(template_file):
        print('Template file error')
        exit(0)

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    html = ''
    with open(template_file, 'r', encoding='utf-8') as f:
        html = f.read()

    with open(src_file, 'r', encoding='utf-8') as f:
        text_array = []
        index = 1
        in_block = False

        for line in f.readlines():
            text = line.strip()

            is_block = False
            if blockquote_start in text:
                in_block = True
                is_block = True
            if blockquote_end in text:
                in_block = False
                is_block = True

            if text == mark_break:
                filename = name_prefix + str(index).zfill(3) + '.xhtml'
                dest_file = os.path.join(output_dir, filename)

                content = ''.join(text_array)
                with open(dest_file, 'w', encoding='utf-8') as f:
                    content = html.format(content)
                    f.write(content)

                text_array.clear()
                index += 1
            else:
                padding_count = 1
                if not is_block and in_block:
                    padding_count = 2
                elif len(line.strip()) == 0:
                    padding_count = 0

                text_array.append(padding * padding_count + line)
