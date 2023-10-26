#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2019 Athanasios Theocharis <athatheoc@gmail.com>
# This was made under ESA Summer of Code in Space 2019
# by Athanasios Theocharis, mentored by Daniel Estevez
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy
from gnuradio import gr
from . import telemetry
import pmt
import array


class telemetry_ocf_adder(gr.basic_block):
    """
    docstring for block telemetry_ocf_adder
    """

    def __init__(self, control_word_type, clcw_version_number, status_field, cop_in_effect,
                 virtual_channel_identification, rsvd_spare1, no_rf_avail, no_bit_lock, lockout, wait,
                 retransmit, farmb_counter, rsvd_spare2, report_value):
        gr.basic_block.__init__(self,
                                name="telemetry_ocf_adder",
                                in_sig=[],
                                out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        self.control_word_type = control_word_type
        self.clcw_version_number = clcw_version_number
        self.status_field = status_field
        self.cop_in_effect = cop_in_effect
        self.virtual_channel_identification = virtual_channel_identification
        self.rsvd_spare1 = rsvd_spare1
        self.no_rf_avail = no_rf_avail
        self.no_bit_lock = no_bit_lock
        self.lockout = lockout
        self.wait = wait
        self.retransmit = retransmit
        self.farmb_counter = farmb_counter
        self.rsvd_spare2 = rsvd_spare2
        self.report_value = report_value

        ##################################################
        # Blocks
        ##################################################
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print()
            "[ERROR] Received invalid message type. Expected u8vector"
            return
        packet = pmt.u8vector_elements(msg)

        finalHeader = array.array('B', telemetry.OCFTrailer.build(dict(control_word_type = self.control_word_type,
                                                                             clcw_version_number = self.clcw_version_number,
                                                                             status_field = self.status_field,
                                                                             cop_in_effect = self.cop_in_effect,
                                                                             virtual_channel_identification = self.virtual_channel_identification,
                                                                             rsvd_spare1 = self.rsvd_spare1,
                                                                             no_rf_avail = self.no_rf_avail,
                                                                             no_bit_lock = self.no_bit_lock,
                                                                             lockout = self.lockout,
                                                                             wait = self.wait,
                                                                             retransmit = self.retransmit,
                                                                             farmb_counter = self.farmb_counter,
                                                                             rsvd_spare2 = self.rsvd_spare2,
                                                                             report_value = self.report_value))).tolist()

        finalPacket = numpy.append(packet, finalHeader)
        finalPacket = array.array('B', finalPacket[:])
        finalPacket = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(finalPacket), finalPacket))
        self.message_port_pub(pmt.intern('out'), finalPacket)
