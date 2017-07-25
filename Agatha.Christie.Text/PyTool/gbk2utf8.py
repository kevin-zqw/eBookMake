# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys

if __name__ == '__main__':
    base_dir = '/Users/kevin/GitHub/eBookMake/zuihoudediqiuzhanshen'

    for filename in os.listdir(base_dir):
        if not filename.endswith('html'):
            continue

        file_path = os.path.join(base_dir, filename)
        text = ''
        with open(file_path, 'r', encoding='gbk') as f:
            text = f.read()
            text.replace('charset=gbk', 'charset=utf-8')

        os.remove(file_path)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
