# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re

base_dir = r'/Users/kevin/GitHub/eBookMake/Agatha.Christie.Text/v29_TheClocks'
# base_dir = r'D:\eBookMake\Agatha.Christie.Text\v29_TheClocks'
book_file_name = r"Unlock-[阿加莎.克里斯蒂侦探推理系列.怪钟].The.Clocks.Agatha.Christie.范白泉.人民文学出版社.2009.中译本扫描版.txt"

pattern_page_no = r'^\d+.{0,4}$'
pattern_book_name = r'^怪钟.{0,4}$'


def open_file_perform(file_path, action):
    with open(file_path, 'r+', encoding='utf-8') as f:
        text = f.read()

        processed_text = action(text)

        f.seek(0)
        f.write(processed_text)
        f.truncate()


def strip_page_no_book_name(text):
    text = re.sub(pattern_page_no, '', text, flags=re.MULTILINE)
    text = re.sub(pattern_book_name, '', text, flags=re.MULTILINE)

    return text


def punctuation(text):
    table = [
        # 基本标点符号
        (r',', r'，'),
        (r'\?', r'？'),
        (r'!', r'！'),
        (r':', r'：'),
        (r';', r'；'),
        (r'\(', r'（'),
        (r'\)', r'）'),
        (r'\[', r'【'),
        (r'\]', r'】'),
        (r'┅', r'…'),

        # 三个以上的.替换为省略号
        (r'\.{3,}', r'……'),
        # 两个.替换为句号
        (r'\.\.', r'。'),
        # 中文后面的.替换为句号
        (r'([^0-9a-zA-Z])\.', r'\1。'),

        # 起始引号”’
        (r'([\u3000\u0020：])"', r'\1“'),
        (r"([\u3000\u0020：])'", r'\1‘'),
    ]

    for pattern, replace in table:
        text = re.sub(pattern, replace, text)

    return text


def proof_reading():
    file_path = os.path.join(base_dir, book_file_name)

    open_file_perform(file_path, strip_page_no_book_name)

    # open_file_perform(file_path, punctuation)


if __name__ == '__main__':
    proof_reading()
