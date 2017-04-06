#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import h5py
import numpy as np

def write_kpoints(kpoints_data, filename):
    with h5py.File(filename, 'w') as f:
        f['type_tag'] = 'kpoints_explicit'
        f['kpoints'] = np.array(kpoints_data.get_kpoints())
