#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import tempfile

import pytest
import numpy as np

from aiida.plugins import DataFactory
from aiida_bands_inspect.io import read, write


@pytest.mark.parametrize(
    'bands_params', [{
        'kpoints': [[0., 0., 0.]],
        'eigenvals': [[0, 1., 2.]]
    }]
)
def test_write_read_bands(configure, bands_params):  # pylint: disable=unused-argument
    BandsData = DataFactory('array.bands')
    bands = BandsData()
    bands.set_kpoints(bands_params['kpoints'])
    bands.set_bands(bands_params['eigenvals'])
    with tempfile.NamedTemporaryFile() as tmpf:
        write(bands, tmpf.name)
        res = read(tmpf.name)
    assert np.allclose(res.get_kpoints(), bands.get_kpoints())
    assert np.allclose(res.get_bands(), bands.get_bands())


def test_write_read_kpoints(configure):  # pylint: disable=unused-argument
    KpointsData = DataFactory('array.kpoints')
    kpoints = KpointsData()
    kpoints.set_kpoints([[0., 0., 0.]])
    with tempfile.NamedTemporaryFile() as tmpf:
        write(kpoints, tmpf.name)
        res = read(tmpf.name)
    assert np.allclose(res.get_kpoints(), kpoints.get_kpoints())


def test_read(configure, sample):  # pylint: disable=unused-argument
    res = read(sample('bands_mesh.hdf5'))
    assert np.allclose(res.get_kpoints(), [[0., 0., 0.], [0., 0., 0.5]])
    assert np.allclose(res.get_bands(), [[1, 2], [3, 4]])
