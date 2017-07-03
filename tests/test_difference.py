#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, unicode_literals

import numpy as np

def test_difference(configure):
    from aiida.orm.code import Code
    from aiida.orm import DataFactory, CalculationFactory
    from aiida.work.run import run

    DifferenceCalculation = CalculationFactory('bandstructure_utils.difference')
    process = DifferenceCalculation.process()
    inputs = process.get_inputs_template()
    inputs.code = Code.get_from_string('bandstructure_utils')
    inputs._options.resources = {'num_machines': 1}
    inputs._options.withmpi = False

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
    assert np.isclose(output['output_parameters'].dict['diff'], 1 / 3)
