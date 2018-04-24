#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals, print_function

import time
import subprocess

import pytest
import numpy as np
from aiida_pytest.markers import skip_caching


@pytest.fixture
def get_bands_builder(get_process_builder):
    from aiida.orm import DataFactory

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


@pytest.fixture
def get_legacy_calc(get_bands_builder):
    def inner():
        from aiida.orm import Code
        from aiida_bands_inspect.calculations.difference import DifferenceCalculation
        calc = DifferenceCalculation()
        builder = get_bands_builder
        inputs = builder._todict()
        for key, value in inputs.items():
            if key.startswith('_') or key in ['dynamic', 'options']:
                continue
            getattr(calc, 'use_{}'.format(key))(value)
        code = Code.get_from_string('bands_inspect')
        calc.use_code(code)
        calc.set_computer(code.get_computer().name)
        calc.set_withmpi(False)
        calc.set_resources({'num_machines': 1})
        return calc

    return inner


def test_difference(configure_with_daemon, get_bands_builder):
    from aiida.work.launch import run_get_node
    from aiida.orm import load_node

    builder = get_bands_builder
    output, calc_node = run_get_node(builder)
    print('State:', calc_node.get_state())
    print('Output:', output)
    print(
        subprocess.check_output(
            ["verdi", "calculation", "logshow", "{}".format(calc_node.pk)],
            stderr=subprocess.STDOUT
        )
    )
    assert np.isclose(output['difference'].value, 1 / 3)


def test_difference_legacy(configure_with_daemon, get_legacy_calc):
    """
    Test DifferenceCalculation through the legacy calculation interface.
    """
    calc = get_legacy_calc()
    calc.store_all()
    calc.submit()
    while not calc.is_finished:
        time.sleep(1)
    assert np.isclose(calc.out.difference.value, 1 / 3)


@skip_caching
def test_difference_cache(
    configure_with_daemon, get_bands_builder, assert_outputs_equal
):
    from aiida.work.launch import run_get_node
    from aiida.orm import load_node
    from aiida.common.caching import enable_caching

    builder = get_bands_builder

    # Fast-forwarding is enabled in the configuration for DifferenceCalculation
    with enable_caching():
        output1, c1 = run_get_node(builder)
        output2, c2 = run_get_node(builder)
    c1.get_hash(ignore_errors=False)
    assert '_aiida_cached_from' in c2.extras()
    assert output1['difference'] == output2['difference']


@skip_caching
def test_difference_legacy_cache(configure_with_daemon, get_legacy_calc):
    """
    Test DifferenceCalculation caching through the legacy calculation interface.
    """
    calc1 = get_legacy_calc()
    calc2 = get_legacy_calc()
    calc1.store_all(use_cache=True)
    if not calc1.is_finished:
        calc1.submit()
    while not calc1.is_finished:
        time.sleep(1)
    calc2.store_all(use_cache=True)
    assert calc2.is_finished
    assert np.isclose(calc1.out.difference.value, calc2.out.difference.value)
    assert '_aiida_cached_from' in calc2.extras()
