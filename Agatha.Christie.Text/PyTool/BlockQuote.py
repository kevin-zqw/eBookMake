# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import shutil
import re
import sys


def process_block_quote(file_path):
    print(file_path)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        return

    file_path = sys.argv[1]
    process_block_quote(file_path)
