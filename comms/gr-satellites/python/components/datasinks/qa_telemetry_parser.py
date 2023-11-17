#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import sys

from gnuradio import gr, blocks, gr_unittest
import numpy as np
import pmt


# bootstrap satellites module, even from build dir
try:
    import python as satellites
except ImportError:
    pass
else:
    import sys
    sys.modules['satellites'] = satellites

from satellites.components.datasinks import telemetry_parser


class qa_telemetry_parser(gr_unittest.TestCase):
    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def test_instance(self):
        """Tries to create a telemetry parser instance

        It uses several combinations of parameters
        """
        definition = 'by02'
        telemetry_parser(definition)
        telemetry_parser(definition, file=sys.stderr)
        telemetry_parser(definition, file='/dev/null')
        telemetry_parser(definition, options='')
        telemetry_parser(definition, options='--telemetry_output /dev/null')


if __name__ == '__main__':
    gr_unittest.run(qa_telemetry_parser)
