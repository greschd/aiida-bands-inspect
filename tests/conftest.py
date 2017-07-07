#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pytest

from aiida_pytest.configure import *
from aiida_pytest.process import *

@pytest.fixture
def sample():
    def inner(name):
        return os.path.join(os.path.abspath('./samples'), name)
    return inner
