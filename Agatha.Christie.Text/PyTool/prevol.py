# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


if __name__ == '__main__':
    # command line parameters
    if len(sys.argv) < 3:
        print('python {} <html_dir> <template_file>'.format(sys.argv[0]))
        exit(1)

    html_dir = sys.argv[1]
    template_file = sys.argv[2]

    if not os.path.exists(html_dir):
        print('html dir not exists!')
        exit(0)

    if not os.path.exists(template_file) or not os.path.isfile(template_file):
        print('template file error!')
        exit(0)

    template = ''
    with open(template_file, 'r', encoding='utf-8') as f:
        template = f.read()

    for filename in os.listdir(html_dir):
        base_name, extension = os.path.splitext(filename)
        if extension != '.html' and extension != '.xhtml' and extension != '.htm':
            continue

        file_path = os.path.join(html_dir, filename)

        result_html = ''
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()

            text = text.replace("<h4", "<h5")
            text = text.replace("</h4>", "</h5>")

            text = text.replace("<h3", "<h4")
            text = text.replace("</h3>", "</h4>")

            text = text.replace("<h2", "<h3")
            text = text.replace("</h2>", "</h3>")

            text = text.replace("<h1", "<h2")
            text = text.replace("</h1>", "</h2>")

            matches = re.findall(r'<body.*?>(.*?)</body>', text, flags=re.DOTALL)
            if len(matches) > 0:
                body = matches[0]
                result_html = template.format(body)

        if len(result_html) > 0:
            output_name = base_name + '.xhtml'
            with open(os.path.join(html_dir, output_name), 'w', encoding='utf-8') as f:
                f.write(result_html)
