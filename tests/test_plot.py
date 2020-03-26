#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import pytest

from aiida.engine.launch import run
from aiida.plugins import DataFactory


@pytest.fixture
def get_plot_builder(get_process_builder):
    builder = get_process_builder(
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

    builder.bands1 = bands1
    builder.bands2 = bands2
    return builder


def test_plot(configure_with_daemon, get_plot_builder):  # pylint: disable=unused-argument
    builder = get_plot_builder
    output = run(builder)
    print(
        'scheduler error file:\n',
        output['retrieved'].open('_scheduler-stderr.txt').read()
    )
    assert 'plot' in output
    assert isinstance(output['plot'], DataFactory('singlefile'))
