#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import pytest

import numpy as np

@pytest.fixture
def bands_process_inputs(get_process_inputs):
    from aiida.orm import DataFactory

    process, inputs = get_process_inputs(
        calculation_string='bands_inspect.difference',
        code_string='bands_inspect'
    )

    BandsData = DataFactory('array.bands')
    bands1 = BandsData()
    bands2 = BandsData()
    kpoints = [[0.1, 0.2, 0.3], [0., 0.5, 0.5]]
    bands1.set_kpoints(kpoints)
    bands2.set_kpoints(kpoints)
    bands1.set_bands([[1, 2, 3], [1, 2, 3]])
    bands2.set_bands([[2, 2, 3], [1, 2, 2]])

    inputs.bands1 = bands1
    inputs.bands2 = bands2
    return process, inputs

def test_difference(configure_with_daemon, bands_process_inputs):
    from aiida.work.run import run

    process, inputs = bands_process_inputs
    output = run(process, **inputs)
    assert np.isclose(output['difference'].value, 1 / 3)

def test_difference_fastforward(configure_with_daemon, bands_process_inputs):
    from aiida.orm import DataFactory
    from aiida.work.run import run
    from aiida.orm import load_node

    process, inputs = bands_process_inputs

    output1, pid1 = run(process, _return_pid=True, _fast_forward=True, **inputs)
    output2, pid2 = run(process, _return_pid=True, _fast_forward=True, **inputs)
    c = load_node(pid1)
    c.get_hash(ignore_errors=False)
    assert pid1 == pid2
    def normalize_output(output):
        return {key: value.uuid for key, value in output.items()}
    assert normalize_output(output1) == normalize_output(output2)
