#!/usr/bin/env python
# -*- coding: utf-8 -*-

# © 2019, Microsoft
# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import pytest
import numpy as np

from aiida.plugins import DataFactory
from aiida.engine.launch import run_get_node
from aiida.manage.caching import enable_caching


@pytest.fixture
def get_bands_builder(get_process_builder):
    builder = get_process_builder(
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

    builder.bands1 = bands1
    builder.bands2 = bands2
    return builder


def test_difference(configure_with_daemon, get_bands_builder):  # pylint: disable=unused-argument
    builder = get_bands_builder
    output, calc_node = run_get_node(builder)

    assert np.isclose(output['difference'].value, 1 / 3)
    assert calc_node.is_finished_ok


def test_difference_cache(
    configure_with_daemon,  # pylint: disable=unused-argument
    get_bands_builder,
):
    builder = get_bands_builder

    # Fast-forwarding is enabled in the configuration for DifferenceCalculation
    with enable_caching():  # pylint: disable=not-context-manager
        output1, c1 = run_get_node(builder)
        output2, c2 = run_get_node(builder)
    c1.get_hash(ignore_errors=False)
    assert '_aiida_cached_from' in c2.extras
    assert output1['difference'] == output2['difference']
