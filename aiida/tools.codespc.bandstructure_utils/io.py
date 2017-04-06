#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import h5py
import numpy as np

def write_kpoints(kpoints_data, filename):
    # This can be replaced with bandstructure_utils.io functions when
    # AiiDA supports Python 3.
    with h5py.File(filename, 'w') as f:
        attrs = kpoints_data.get_attrs()
        if 'mesh' in attrs:
            f['type_tag'] = 'kpoints_mesh'
            f['mesh'] = np.array(attrs['mesh'])
            f['offset'] = np.array(attrs['offset'])
        elif 'array|kpoints' in attrs:
            f['type_tag'] = 'kpoints_explicit'
            f['kpoints'] = np.array(kpoints_data.get_kpoints())
        else:
            raise NotImplementedError("Unrecognized KpointsData form, has attrs '{}'".format(attrs))
