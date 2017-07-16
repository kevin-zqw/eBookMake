# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re


if __name__ == '__main__':
    src_file = r'/Users/kevin/Downloads/中国鬼神精怪 - 副本.txt'
    with open(src_file, 'r', encoding='utf-8') as f:
        all_text = f.read()
        matcher = re.findall(r'（(出.*)）', all_text)

        print(len(matcher))
        result = []
        for text in matcher:
            if text not in result:
                result.append(text)

        print(len(result))
        print(result)

        output = r'/Users/kevin/Downloads/书目.txt'
        with open(output, 'w', encoding='utf-8') as f:
            f.write('\n'.join(result))
