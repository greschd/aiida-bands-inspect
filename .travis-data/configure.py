#!/usr/bin/env python
"""
Usage: python configure.py travis_data_folder test_folder
"""

import sys
import subprocess
from os.path import join

travis_data_folder = sys.argv[1]
in_file = join(travis_data_folder, 'test_config.yml')
bands_inspect_path = subprocess.check_output(
    'which bands-inspect', shell=True
).decode().strip()

out_file = join(sys.argv[2], 'config.yml')

with open(in_file, 'r') as f:
    res = f.read().format(bands_inspect_path=bands_inspect_path)
with open(out_file, 'w') as f:
    f.write(res)
