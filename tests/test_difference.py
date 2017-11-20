#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals, print_function

import time

import pytest
import numpy as np
from aiida_pytest.markers import skip_caching


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


@pytest.fixture
def get_legacy_calc(bands_process_inputs):
    def inner():
        from aiida.orm import Code
        from aiida_bands_inspect.calculations.difference import DifferenceCalculation
        calc = DifferenceCalculation()
        _, inputs = bands_process_inputs
        for key, value in inputs.items():
            if key.startswith('_') or key in ['dynamic']:
                continue
            getattr(calc, 'use_{}'.format(key))(value)
        code = Code.get_from_string('bands_inspect')
        calc.use_code(code)
        calc.set_computer(code.get_computer().name)
        calc.set_withmpi(False)
        calc.set_resources({'num_machines': 1})
        return calc

    return inner


def test_difference(configure_with_daemon, bands_process_inputs):
    from aiida.work.run import run
    from aiida.orm import load_node

    process, inputs = bands_process_inputs
    output, pid = run(process, _use_cache=False, _return_pid=True, **inputs)
    calc_node = load_node(pid)
    print('State:', calc_node.get_state())
    print(output)
    import subprocess
    try:
        assert np.isclose(output['difference'].value, 1 / 3)
    except Exception as e:
        print(
            subprocess.check_output(
                ["verdi", "calculation", "logshow", "{}".format(pid)],
                stderr=subprocess.STDOUT
            )
        )
        raise e


def test_difference_legacy(configure_with_daemon, get_legacy_calc):
    """
    Test DifferenceCalculation through the legacy calculation interface.
    """
    calc = get_legacy_calc()
    calc.store_all()
    calc.submit()
    while not calc.has_finished():
        time.sleep(1)
    assert np.isclose(calc.out.difference.value, 1 / 3)


@skip_caching
def test_difference_cache(
    configure_with_daemon, bands_process_inputs, assert_outputs_equal
):
    from aiida.work.run import run
    from aiida.orm import load_node

    process, inputs = bands_process_inputs

    # Fast-forwarding is enabled in the configuration for DifferenceCalculation
    output1, pid1 = run(process, _return_pid=True, **inputs)
    output2, pid2 = run(process, _return_pid=True, **inputs)
    c1 = load_node(pid1)
    c2 = load_node(pid1)
    c1.get_hash(ignore_errors=False)
    assert 'cached_from' in c2.extras()
    assert output1['difference'] == output2['difference']


@skip_caching
def test_difference_legacy_cache(configure_with_daemon, get_legacy_calc):
    """
    Test DifferenceCalculation caching through the legacy calculation interface.
    """
    calc1 = get_legacy_calc()
    calc2 = get_legacy_calc()
    calc1.store_all(use_cache=True)
    if not calc1.has_finished():
        calc1.submit()
    while not calc1.has_finished():
        time.sleep(1)
    calc2.store_all(use_cache=True)
    assert calc2.has_finished()
    assert np.isclose(calc1.out.difference.value, calc2.out.difference.value)
    assert 'cached_from' in calc2.extras()
