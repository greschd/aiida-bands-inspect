#!/usr/bin/env python
# -*- coding: utf-8 -*-

def test_difference(config):
    from aiida.orm.code import Code
    c = Code.get_from_string('bandstructure_utils')
    assert c.is_stored
