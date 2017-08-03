# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys

dict_file = r'/Users/kevin/GitHub/eBookMake/Agatha.Christie.Text/PyTool/常见词语错误.txt'
pattern_dict_line = r'"(.+)"\s*→\s*"(.+)"'

pattern_page_no = r'^[\^\d]+.{0,5}$'

ending_punctuation = r'.<>/?;:{}"()\[\]。《》？！；：‘’“”（）·【】……\n'.format("'")
pattern_hard_break = r'(.{}[^{}]+)\n+([\u4e00-\u9fa5]+)'.format('{5,}', ending_punctuation)
replace_hard_break = r'\1\2'


def open_file_perform(file_path, action, line_mode=False):
    with open(file_path, 'r+', encoding='utf-8') as f:
        if line_mode:
            processed_text = action(f.readlines())
        else:
            processed_text = action(f.read())

        f.seek(0)
        f.write(processed_text)
        f.truncate()


def strip_page_no_book_name(text):
    text = re.sub(pattern_page_no, '', text, flags=re.MULTILINE)

    return text


def base_punctuation(text):
    table = [
        # 基本标点符号
        (r',', r'，'),
        (r'\?', r'？'),
        (r'!', r'！'),
        (r':', r'：'),
        (r';', r'；'),
        (r'\(', r'（'),
        (r'\)', r'）'),
        (r'<', r'《'),
        (r'>', r'》'),
        (r'&', r''),

        # 重复引号
        (r'‘‘', r'“'),
        (r'’’', r'”'),

        # 破折号
        (r'-一', r'——'),
        (r'一-', r'——'),
        (r'----', r'——'),
        (r'---', r'——'),
        (r'--', r'——'),
        (r'—-', r'——'),
        (r'-—', r'——'),

        # 三个以上的.替换为省略号
        (r'\.{3,}', r'……'),

        # 两个.替换为句号
        (r'\.\.', r'。'),

        # 中文后面的.替换为句号
        (r'([^0-9a-zA-Z])\.', r'\1。'),
    ]

    for pattern, replace in table:
        text = re.sub(pattern, replace, text)

    return text


def fix_line_break(text):
    text = re.sub(pattern_hard_break, replace_hard_break, text)

    return text


def fix_quotation_marks(all_lines):
    single_q_open = '‘'
    single_q_close = '’'
    double_q_open = '“'
    double_q_close = '”'

    processed_lines = []

    for line in all_lines:
        next_single_open = True
        next_double_open = True

        fixed_line = []
        for ch in line:
            if ch == single_q_open:
                next_single_open = False
            if ch == double_q_open:
                next_double_open = False

            if ch == "'":
                if next_single_open:
                    ch = single_q_open
                else:
                    ch = single_q_close

                next_single_open = not next_single_open

            if ch == '"':
                if next_double_open:
                    ch = double_q_open
                else:
                    ch = double_q_close

                next_double_open = not next_double_open

            fixed_line.append(ch)

        processed_lines.append(''.join(fixed_line))

    return ''.join(processed_lines)


def fix_words_error(text):
    with open(dict_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            matcher = (re.match(pattern_dict_line, line))
            if matcher:
                old = matcher.group(1)
                new = matcher.group(2)

                if len(old) > 0 and len(new) > 0:
                    text = text.replace(old, new)

    return text


def proof_reading():
    if len(sys.argv) < 2:
        print('usage: python {} <file_path>'.format(sys.argv[0]))
        exit(-1)

    file_path = sys.argv[1]

    open_file_perform(file_path, strip_page_no_book_name)

    open_file_perform(file_path, base_punctuation)
    open_file_perform(file_path, fix_line_break)
    open_file_perform(file_path, fix_quotation_marks, line_mode=True)

    open_file_perform(file_path, fix_words_error)


if __name__ == '__main__':
    proof_reading()
