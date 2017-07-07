#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import numpy as np

def test_difference(configure_with_daemon, get_process_inputs):
    from aiida.orm import DataFactory
    from aiida.work.run import run

    process, inputs = get_process_inputs(
        calculation_string='bandstructure_utils.difference',
        code_string='bandstructure_utils'
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

    output = run(process, **inputs)
    assert np.isclose(output['difference'].value, 1 / 3)
