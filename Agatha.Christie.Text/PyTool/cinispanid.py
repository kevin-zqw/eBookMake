# -*- coding: utf-8 -*-
__author__ = 'kevin'

from bs4 import BeautifulSoup
import os
import re

if __name__ == '__main__':
    path = r'/Users/kevin/Downloads/Chapter1_3.xhtml'

    with open(path, 'r+', encoding="utf-8") as file:
        text = file.read()

        span = '<span id="jgj">'
        index = 1
        while text.find(span) != -1:
            new_span = '<span id="jgj{}">'.format(str(index).zfill(3))
            index += 1
            text = text.replace(span, new_span, 1)

        file.seek(0)
        file.write(text)
        file.truncate()
