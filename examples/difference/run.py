#!/usr/bin/env runaiida
# -*- coding: utf-8 -*-

# © 2017-2019, ETH Zurich, Institut für Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

from __future__ import division, print_function, unicode_literals

from aiida.orm import Code
from aiida.plugins import DataFactory, CalculationFactory
from aiida.engine import run


def main():
    DifferenceCalculation = CalculationFactory('bands_inspect.difference')
    builder = DifferenceCalculation.get_builder()
    builder.code = Code.get_from_string('bands_inspect')
    builder.metadata.options = dict(
        resources={'num_machines': 1}, withmpi=False
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

    output = run(builder)
    print('Difference:', output['difference'])


if __name__ == '__main__':
    main()
