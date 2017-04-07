#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import h5py
import numpy as np

from aiida.orm import DataFactory

def write_kpoints(kpoints_data, filename):
    """
    Write a 'KpointsData' instance to a file in bandstructure_utils HDF5 format.
    """
    # This can be replaced with bandstructure_utils.io functions when
    # AiiDA supports Python 3.
    with h5py.File(filename, 'w') as f:
        _serialize_kpoints(kpoints_data, f)

def _serialize_kpoints(kpoints_data, hdf5_handle):
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

def read_bands(filename):
    """
    Read a HDF5 in bandstructure_utils HDF5 format containing an EigenvalsData instance, and return an AiiDA BandsData instance.
    """
    with h5py.File(filename, 'r') as f:
        kpoints = _parse_kpoints(f['kpoints_obj'])
        # BandsData cannot have a mesh as k-points...
        bands = DataFactory('array.bands')()
        bands.set_kpoints(kpoints.get_kpoints_mesh(print_list=True))
        bands.set_bands(f['eigenvals'].value)
    return bands

def _parse_kpoints(hdf5_handle):
    type_tag = hdf5_handle['type_tag'].value
    kpoints = DataFactory('array.kpoints')()
    if type_tag == 'kpoints_mesh':
        kpoints.set_kpoints_mesh(
            hdf5_handle['mesh'].value,
            hdf5_handle['offset'].value
        )
    elif type_tag == 'kpoints_explicit':
        kpoints.set_kpoints(
            hdf5_handle['kpoints'].value
        )
    else:
        raise NotImplementedError("Unrecognized type_tag '{}' encountered when parsing k-points data.".format(type_tag))
    return kpoints

def write_bands(bands_data, filename):
    """
    Write a 'BandsData' instance to a file in bandstructure_utils HDF5 format.
    """
    with h5py.File(filename, 'w') as f:
        kpt = f.create_group('kpoints_obj')
        _serialize_kpoints(bands_data, kpt)
        f['eigenvals'] = bands_data.get_bands()
        f['type_tag'] = 'eigenvals_data'
