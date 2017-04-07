#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from aiida.orm import JobCalculation, DataFactory
from aiida.common.utils import classproperty
from aiida.common.exceptions import InputValidationError
from aiida.common.datastructures import CalcInfo, CodeInfo

class DifferenceCalculation(JobCalculation):
    @classproperty
    def _use_methods(cls):
        retdict = super(cls, cls)._use_methods
        retdict['bands'] = dict(
            valid_types=DataFactory('array.bands'),
            additional_parameter=1,
            linkname='bands',
            docstring="Bandstructures which are to be compared"
        )
        return retdict

    # def _prepare_for_submission(self, tempfolder, inputdict):
