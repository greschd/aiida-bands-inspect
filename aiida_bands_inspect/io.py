#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>
"""
Defines functions for reading and writing bands-inspect HDF5 files
from / to AiiDA Data nodes.
"""

import warnings

from aiida import orm
from bands_inspect.io import save, load

from .convert import from_bands_inspect, to_bands_inspect

__all__ = ('read', 'write')


def write(data: orm.Data, filename: str) -> None:
    """
    Write an AiiDA Data instance to a file in bands_inspect HDF5 format.

    Parameters
    ----------
    data :
        The AiiDA data instance to be written.
    filename :
        Path of the file being written to.
    """
    save(to_bands_inspect(data), hdf5_file=filename)


def write_kpoints(kpoints_data, filename):
    """
    .. note:: This function is deprecated, use :func:`write` instead.

    Write an AiiDA Data instance to a file in bands_inspect HDF5 format.

    Parameters
    ----------
    data :
        The AiiDA data instance to be written.
    filename :
        Path of the file being written to.
    """
    warnings.warn(
        "The 'write_kpoints' function is deprecated, use 'write' instead",
        DeprecationWarning
    )
    write(data=kpoints_data, filename=filename)


def write_bands(bands_data, filename):
    """
    .. note:: This function is deprecated, use :func:`write` instead.

    Write an AiiDA Data instance to a file in bands_inspect HDF5 format.

    Parameters
    ----------
    data :
        The AiiDA data instance to be written.
    filename :
        Path of the file being written to.
    """
    warnings.warn(
        "The 'write_bands' function is deprecated, use 'write' instead",
        DeprecationWarning
    )
    write(data=bands_data, filename=filename)


def read(filename: str) -> orm.Data:
    """
    Read a HDF5 file in bands_inspect format, and return a corresponding
    AiiDA Data instance.

    Parameters
    ----------
    filename : str
        Path of the file to be read.
    """
    return from_bands_inspect(load(hdf5_file=filename))


def read_kpoints(filename):
    """
    .. note:: This function is deprecated, use :func:`read` instead.

    Read a HDF5 file in bands_inspect format, and return a corresponding
    AiiDA Data instance.

    Parameters
    ----------
    filename : str
        Path of the file to be read.
    """
    warnings.warn(
        "The 'read_kpoints' function is deprecated, use 'read' instead",
        DeprecationWarning
    )
    return read(filename)


def read_bands(filename):
    """
    .. note:: This function is deprecated, use :func:`read` instead.

    Read a HDF5 file in bands_inspect format, and return a corresponding
    AiiDA Data instance.

    Parameters
    ----------
    filename : str
        Path of the file to be read.
    """
    warnings.warn(
        "The 'read_bands' function is deprecated, use 'read' instead",
        DeprecationWarning
    )
    return read(filename)
