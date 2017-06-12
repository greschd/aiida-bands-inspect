#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:  Dominik Gresch <greschd@gmx.ch>

from aiida.orm import DataFactory
from aiida.parsers.parser import Parser

class DifferenceParser(Parser):
    """
    Parse bandstructure_utils difference output to float.
    """
    def parse_with_retrieved(self, retrieved):
        try:
            out_folder = retrieved[self._calc._get_linkname_retrieved()]
        except KeyError:
            self.logger.error("No retrieved folder found")

        with open(out_folder.get_abs_path(self._calc._OUTPUT_FILE_NAME), 'r') as f:
            res = float(f.read())

        output_data = DataFactory('parameter')(dict=dict(diff=res))
        new_nodes_list = [(self.get_linkname_outparams(), output_data)]

        return True, new_nodes_list
