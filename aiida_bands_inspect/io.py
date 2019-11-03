#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

import h5py
import numpy as np

from aiida.plugins import DataFactory


def write_kpoints(kpoints_data, *args, **kwargs):
    """
    Write a 'KpointsData' instance to a file or file-like object in bands_inspect HDF5 format. Except for ``kpoints_data``, all positional
    and keyword arguments are passed to :class:`h5py.File`.
    """
    # This can be replaced with bands_inspect.io functions when
    # AiiDA supports Python 3.
    with h5py.File(*args, **kwargs) as f:
        _serialize_kpoints(kpoints_data, f)


def _serialize_kpoints(kpoints_data, hdf5_handle):
    attrs = kpoints_data.attributes
    if 'mesh' in attrs:
        hdf5_handle['type_tag'] = 'kpoints_mesh'
        hdf5_handle['mesh'] = np.array(attrs['mesh'])
        hdf5_handle['offset'] = np.array(attrs['offset'])
    elif 'array|kpoints' in attrs:
        hdf5_handle['type_tag'] = 'kpoints_explicit'
        hdf5_handle['kpoints'] = np.array(kpoints_data.get_kpoints())
    else:
        raise NotImplementedError(
            "Unrecognized KpointsData form, has attrs '{}'".format(attrs)
        )


def read_bands(*args, **kwargs):
    """
    Read a HDF5 in bands_inspect HDF5 format containing an EigenvalsData
    instance, and return an AiiDA BandsData instance. Positional and keyword
    arguments are passed to :class:`h5py.File`.
    """
    with h5py.File(*args, **kwargs) as f:
        kpoints = _parse_kpoints(f['kpoints_obj'])
        # BandsData cannot have a mesh as k-points...
        bands = DataFactory('array.bands')()
        if 'mesh' in kpoints.attributes:
            bands.set_kpoints(kpoints.get_kpoints_mesh(print_list=True))
        else:
            bands.set_kpointsdata(kpoints)
        bands.set_bands(f['eigenvals'].value)
    return bands


def _parse_kpoints(hdf5_handle):
    type_tag = hdf5_handle['type_tag'].value
    kpoints = DataFactory('array.kpoints')()
    if 'kpoints_mesh' in type_tag:
        kpoints.set_kpoints_mesh(
            hdf5_handle['mesh'].value, hdf5_handle['offset'].value
        )
    elif 'kpoints_explicit' in type_tag:
        kpoints.set_kpoints(hdf5_handle['kpoints'].value)
    else:
        raise NotImplementedError(
            "Unrecognized type_tag '{}' encountered when parsing k-points data."
            .format(type_tag)
        )
    return kpoints


def write_bands(bands_data, filename):
    """
    Write a 'BandsData' instance to a file in bands_inspect HDF5 format.
    """
    with h5py.File(filename, 'w') as f:
        kpt = f.create_group('kpoints_obj')
        _serialize_kpoints(bands_data, kpt)
        bands_arr = bands_data.get_bands()
        if len(bands_arr.shape) == 3:
            assert bands_arr.shape[0] == 1
            bands_arr = bands_arr[0, :, :]
        f['eigenvals'] = bands_arr
        f['type_tag'] = 'bands_inspect.eigenvals_data'
