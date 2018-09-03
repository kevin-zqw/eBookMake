# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


def process_api():
    source_file = '/Users/kevin/GitHub/eBookMake/Agatha.Christie.Text/PyTool/api.txt'

    url_list = []
    api_list = []
    all_fields = []

    with open(source_file, 'r', encoding='utf-8') as f:
        url = ''
        api = ''
        fields = []

        for line in f.readlines():
            url_api = re.findall(r'@POST\(("/app/user/(.*?)")\)', line)
            if len(url_api) > 0:
                url = url_api[0][0]
                api = url_api[0][1]
                url_list.append(url)
                api_list.append(api)

                if len(fields) > 0:
                    all_fields.append(fields)
                fields = []

            for field_rs in re.findall(r'@Field\("(.*?)"\)\s*(.*?)\s+.*?[,)]', line):
                fields.append(field_rs)

        if len(fields) > 0:
            all_fields.append(fields)

    base_url_rs = ''
    path_rs = []
    let_pa_rs = []
    for idx, api in enumerate(api_list):
        case_str = 'case ' + api + '(' + params(all_fields[idx]) + ')'
        print(case_str)

        base_url_rs += '.' + api + ', '

        path = 'case .' + api + ':\nreturn ' + url_list[idx]
        path_rs.append(path)

        let_pa = 'case .' + api + '(' + let_params(all_fields[idx]) + '):\n'
        let_pa += 'return [\n'
        let_pa += query_param(all_fields[idx])
        let_pa += '\n]'
        let_pa_rs.append(let_pa)

    print('\n\n\n')
    print(base_url_rs)
    print('\n\n\n')
    for path in path_rs:
        print(path)
    print('\n\n\n')
    for let in let_pa_rs:
        print(let)


def params(fields):
    pa_list = []
    for f, t in fields:
        if t != 'String':
            t = 'Int'
        pa = f + ': ' + t
        pa_list.append(pa)

    return ', '.join(pa_list)


def let_params(fields):
    pa_list = []
    for f, t in fields:
        pa = 'let ' + f
        pa_list.append(pa)

    return ', '.join(pa_list)


def query_param(fields):
    pa_list = []
    for f, t in fields:
        value = f
        if t != 'String':
            value = 'String(' + f + ')'
        pa = '("' + f + '", ' + value + ')'
        pa_list.append(pa)

    return ',\n'.join(pa_list)


if __name__ == '__main__':
    process_api()
