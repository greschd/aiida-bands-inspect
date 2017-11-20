#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import pytest


@pytest.fixture
def plot_process_inputs(get_process_inputs):
    from aiida.orm import DataFactory

    process, inputs = get_process_inputs(
        calculation_string='bands_inspect.plot', code_string='bands_inspect'
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


def test_plot(configure_with_daemon, plot_process_inputs):
    from aiida.work.run import run
    from aiida.orm import DataFactory

    process, inputs = plot_process_inputs
    output = run(process, _use_cache=False, **inputs)
    assert 'plot' in output
    assert isinstance(output['plot'], DataFactory('singlefile'))
