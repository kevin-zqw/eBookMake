# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re

base_dir = r'/Users/kevin/GitHub/eBookMake/Agatha.Christie.Text'
# base_dir = r'D:\eBookMake\Agatha.Christie.Text'
book_file_name = r"Unlock-[阿加莎.克里斯蒂侦探推理系列.悬崖上的谋杀].Why.Didn't.They.Ask.Evans.Agatha.Christie.叶刚.人民文学出版社.2010.中译本扫描版.txt"
book_dir_name = r'v64_WhyDidntTheyAskEvans'
chapter_file_name_template = r'v64ch{0}.xhtml'
chapter_file_start_no = 1

output_dir = os.path.join(base_dir, 'output')
process_file = os.path.join(base_dir, book_dir_name, book_file_name)
html_template_file = os.path.join(base_dir, r'Templates', r'base_html.xhtml')

duokan_comment_ref_template = '<sup><a class="duokan-footnote" href="#footnote{}" id="note{}"><img alt="注" src="../Images/note.png"/></a></sup>'
duokan_comment_define_template = '    <li class="duokan-footnote-item" id="footnote{}"><a href="#note{}">{}</a></li>'
duokan_comment_start = '<ol class="duokan-footnote-content hr"></ol>\n\n  <ol class="duokan-footnote-content">'
duokan_comment_end = '</ol>'

page_break = '【PAGE_BREAK】'
pattern_chapter_no_name = r'【CHAPTER_NO[：:](.*?)】【CHAPTER_NAME[：:](.*?)】'
pattern_duokan_comment = r'(【DUOKAN_COMMENT[：:](.*?)】)'

replace_chapter_no = r'【CHAPTER_NO】'
replace_chapter_name = r'【CHAPTER_NAME】'
replace_chapter_text = r'【CHAPTER_TEXT】'

replace_duokan_comment_start = r'【DUOKAN_COMMENT_START】'
replace_duokan_comment_end = r'【DUOKAN_COMMENT_END】'
replace_duokan_comment_list = r'【DUOKAN_COMMENT】'


def get_chapter_file_name(chapter_index):
    return chapter_file_name_template.format('{:02d}'.format(chapter_index))


def get_base_html():
    with open(html_template_file, 'r', encoding="utf-8") as f:
        return f.read()


def beautiful_lines(chapter_lines):
    start_index = 0
    for i in range(len(chapter_lines)):
        text = chapter_lines[i]
        if len(text.strip()) == 0:
            start_index = i
        else:
            break

    last_index = len(chapter_lines)
    for i in reversed(range(last_index)):
        text = chapter_lines[i]
        if len(text.strip()) == 0:
            last_index = i
        else:
            break

    result_lines = []
    for text in chapter_lines[start_index:last_index]:
        result_lines.append('  ' + text)

    return result_lines


def save_html_file(chapter_lines, duokan_comment, chapter_no, chapter_index, chapter_name):
    chapter_lines = beautiful_lines(chapter_lines)
    if len(chapter_lines) == 0:
        return

    html = get_base_html()

    html = html.replace(replace_chapter_no, chapter_no)
    html = html.replace(replace_chapter_name, chapter_name)

    chapter_text = '\n'.join(chapter_lines)
    html = html.replace(replace_chapter_text, chapter_text)

    if len(duokan_comment) > 0:
        comment_text = '\n\n'.join(duokan_comment)
        html = html.replace(replace_duokan_comment_start, duokan_comment_start)
        html = html.replace(replace_duokan_comment_list, comment_text)
        html = html.replace(replace_duokan_comment_end, duokan_comment_end)
    else:
        html = html.replace(replace_duokan_comment_start, '')
        html = html.replace(replace_duokan_comment_list, '')
        html = html.replace(replace_duokan_comment_end, '')

    # write to output dir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    file_name = get_chapter_file_name(chapter_index)
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        print(file_path)
        f.write(html)


def all_process():
    with open(process_file, 'r', encoding="utf-8") as f:
        all_lines = f.readlines()

        chapter_lines = []
        duokan_comment = []
        comment_index = 1
        chapter_no = ''
        chapter_name = ''
        chapter_index = chapter_file_start_no

        for line in all_lines:
            line = line.strip()
            chapter_started = len(chapter_lines) > 0

            if page_break in line and chapter_started:
                save_html_file(chapter_lines, duokan_comment, chapter_no, chapter_index, chapter_name)
                chapter_index += 1

                # clear for next chapter
                chapter_lines.clear()
                duokan_comment.clear()
                comment_index = 1
                chapter_no = ''
                chapter_name = ''
                continue

            if len(line) == 0:
                if chapter_started:
                    chapter_lines.append(line)
                continue

            chapter_groups = re.findall(pattern_chapter_no_name, line)
            if len(chapter_groups) > 0:
                chapter_no, chapter_name = chapter_groups[0]
                continue

            if not line.startswith('<'):
                line = '<p>' + line + '</p>'

            comment_groups = re.findall(pattern_duokan_comment, line)
            for comment_tag, comment_text in comment_groups:
                line = line.replace(comment_tag, duokan_comment_ref_template.format(comment_index, comment_index))
                duokan_comment.append(duokan_comment_define_template.format(comment_index, comment_index, comment_text))
                comment_index += 1

            chapter_lines.append(line)

        # save the last chapter
        save_html_file(chapter_lines, duokan_comment, chapter_no, chapter_index, chapter_name)


if __name__ == '__main__':
    all_process()
