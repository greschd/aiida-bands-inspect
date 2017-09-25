#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile

import pytest
import numpy as np


@pytest.mark.parametrize(
    'bands_params', [{
        'kpoints': [[0., 0., 0.]],
        'eigenvals': [[0, 1., 2.]]
    }]
)
def test_write_read(configure, bands_params):
    from aiida.orm import DataFactory
    from aiida_bands_inspect.io import read_bands, write_bands
    BandsData = DataFactory('array.bands')
    bands = BandsData()
    bands.set_kpoints(bands_params['kpoints'])
    bands.set_bands(bands_params['eigenvals'])
    with tempfile.NamedTemporaryFile() as tmpf:
        write_bands(bands, tmpf.name)
        res = read_bands(tmpf.name)
    assert np.allclose(res.get_kpoints(), bands.get_kpoints())
    assert np.allclose(res.get_bands(), bands.get_bands())


def test_read(configure, sample):
    from aiida_bands_inspect.io import read_bands
    res = read_bands(sample('bands_mesh.hdf5'))
    assert np.allclose(res.get_kpoints(), [[0., 0., 0.], [0., 0., 0.5]])
    assert np.allclose(res.get_bands(), [[1, 2], [3, 4]])
