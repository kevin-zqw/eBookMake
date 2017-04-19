# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re

# base_dir = r'/Users/kevin/GitHub/eBookMake/Agatha.Christie.Text'
base_dir = r'D:\eBookMake\Agatha.Christie.Text'
book_file_name = r"Unlock-[阿加莎.克里斯蒂侦探推理系列.悬崖上的谋杀].Why.Didn't.They.Ask.Evans.Agatha.Christie.叶刚.人民文学出版社.2010.中译本扫描版.txt"
book_dir_name = r'v64_WhyDidntTheyAskEvans'
chapter_file_name_template = r'v64ch{0}.xhtml'

output_dir = os.path.join(base_dir, 'output')
process_file = os.path.join(base_dir, book_dir_name, book_file_name)
html_template_file = os.path.join(base_dir, r'Templates', r'base_html.xhtml')

page_break = '【PAGE_BREAK】'
pattern_chapter_no_name = r'【CHAPTER_NO:(\d+)】【CHAPTER_NAME:(.+)】'
pattern_duokan_comment = r'【DUOKAN_COMMENT\:.*?】'

replace_chapter_no = r'【CHAPTER_NO】'
replace_chapter_name = r'【CHAPTER_NAME】'
replace_chapter_text = r'【CHAPTER_TEXT】'
replace_duokan_comment = r'【DUOKAN_COMMENT】'


def get_chapter_file_name(chapter_no):
    return chapter_file_name_template.format(chapter_no.zfill(2))


def get_base_html():
    with open(html_template_file, 'r', encoding="utf-8") as f:
        return f.read()


# return list of duokan comment string
def process_duokan_comment(chapter):
    all_comments = re.findall(pattern_duokan_comment, chapter)
    if len(all_comments) == 0:
        return []

    for comment in all_comments:
        print(comment)


def save_html_file():
    print('save')


def all_process():
    with open(process_file, 'r', encoding="utf-8") as f:
        all_lines = f.readlines()

        chapter_lines = []
        duokan_comment = []
        chapter_no = ''
        chapter_name = ''
        for line in all_lines:
            chapter_started = len(chapter_lines) > 0
            empty_line = len(line.strip()) == 0

            if page_break in line and chapter_started:
                save_html_file()
                chapter_lines.clear()
                duokan_comment.clear()
                continue

            if empty_line and not chapter_started:
                continue

            chapter_groups = re.findall(pattern_chapter_no_name, line)
            if len(chapter_groups) > 0:
                chapter_no = chapter_groups[0][0]
                chapter_name = chapter_groups[0][1]
                continue

            print(line)


if __name__ == '__main__':
    all_process()
