#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from gnuradio import gr
import numpy as np
import pmt

from .eseo_line_decoder import reflect_bytes


class eseo_packet_crop(gr.basic_block):
    """docstring for block eseo_packet_crop"""
    def __init__(self, drop_rs):
        gr.basic_block.__init__(
            self,
            name='eseo_packet_handler',
            in_sig=[],
            out_sig=[])

        self.drop_rs = drop_rs

        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print('[ERROR] Received invalid message type. Expected u8vector')
            return
        packet = bytes(pmt.u8vector_elements(msg))

        # Find packet end marker
        idx = packet.find(b'\x7e\x7e')
        if idx == -1:
            return
        crop = idx if not self.drop_rs else idx - 16
        if crop < 0:
            return

        # Reverse byte ordering
        packet = np.frombuffer(packet[:crop], dtype='uint8')
        packet = np.packbits(reflect_bytes(np.unpackbits(packet)))
        packet = bytes(packet)

        self.message_port_pub(pmt.intern('out'),
                              pmt.cons(pmt.car(msg_pmt),
                                       pmt.init_u8vector(len(packet), packet)))
