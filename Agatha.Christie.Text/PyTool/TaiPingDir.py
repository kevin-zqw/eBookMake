# -*- coding: utf-8 -*-
__author__ = 'kevin'

import os
import re


if __name__ == '__main__':
    base_dir = r'/Users/kevin/GitHub/eBookMake/taipinguangji/ctext.org/taiping-guangji'

    for filename in os.listdir(base_dir):
        new_name = filename.zfill(3)

        if filename != new_name:
            src_path = os.path.join(base_dir, filename)
            dest_path = os.path.join(base_dir, new_name)

            os.rename(src_path, dest_path)
        