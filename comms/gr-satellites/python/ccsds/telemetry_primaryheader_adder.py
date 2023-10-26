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
import pmt
from . import telemetry
import array
from collections import deque

class telemetry_primaryheader_adder(gr.basic_block):
    """space_packet_parser
    docstring for block telemetry_primaryheader_adder
    """
    def __init__(self, transfer_frame_version_number, spacecraft_id, virtual_channel_id, ocf_flag, master_channel_frame_count,
                 virtual_channel_frame_count, transfer_frame_secondary_header_flag, synch_flag, packet_order_flag, segment_length_id,
                 first_header_pointer, coding, reed_solomon_concat, e, q, I, turbo, ldpc_tf, ldpc_tf_size, num_of_octets):
        gr.basic_block.__init__(self,
            name="telemetry_primaryheader_adder",
            in_sig=[],
            out_sig=[])

        ##################################################
        # Parameters
        ##################################################
        num_of_octets += 1
        self.transfer_frame_version_number = 0
        self.spacecraft_id = spacecraft_id
        self.virtual_channel_id = virtual_channel_id
        self.ocf_flag = ocf_flag
        self.master_channel_frame_count = master_channel_frame_count
        self.virtual_channel_frame_count = virtual_channel_frame_count
        self.transfer_frame_secondary_header_flag = transfer_frame_secondary_header_flag
        self.synch_flag = synch_flag
        self.packet_order_flag = packet_order_flag
        self.segment_length_id = segment_length_id
        self.first_header_pointer = 0
        self.coding = coding
        self.reed_solomon_concat = reed_solomon_concat
        self.e = e
        self.q = q
        self.I = I
        self.turbo = turbo
        self.ldpc_tf = ldpc_tf
        self.ldpc_tc_size = ldpc_tf_size
        self.num_of_octets = num_of_octets
        ##################################################
        # Variables
        ##################################################
        self.list = []
        self.size = self.calculateSize()
        ##################################################
        # Blocks
        ##################################################
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        if not pmt.is_u8vector(msg):
            print("[ERROR] Received invalid message type. Expected u8vector")
            return
        packet = pmt.u8vector_elements(msg)

        next_pointer = 0

        while len(packet) > 0:
            limit = self.size - len(self.list)
            if len(packet) > limit:
                if len(packet) >= limit + self.size:
                    next_pointer = 0x3ff
                else:
                    next_pointer = len(packet) - limit
            elif len(packet) == limit:
                next_pointer = 0

            self.list.extend(packet[:limit])
            packet = packet[limit:]

            if len(self.list) == self.size:
                finalPacket = numpy.append(self.calculateFinalHeader(), self.list)
                self.sendPacket(finalPacket)
                self.list = []
                self.first_header_pointer = next_pointer

    def sendPacket(self, packet):
        packet = array.array('B', packet[:])
        packet = pmt.cons(pmt.PMT_NIL, pmt.init_u8vector(len(packet), packet))
        self.message_port_pub(pmt.intern('out'), packet)

    def calculateSize(self):
        if self.coding == 1 or self.coding == 2 or self.coding == 7:
            size = self.num_of_octets
        elif self.coding == 3 or self.coding == 4:
            size = (255 - 2 * self.e - self.q) * self.I

            if self.reed_solomon_concat == 0:
                if ((255-self.q)*self.I)%4!=0:
                    print("Codeblock (255-q)*I is not a multiple of 4")
        elif self.coding == 5:
            size = self.turbo
        else:
            if self.ldpc_tf < 3:
                size = self.ldpc_tc_size
            else:
                size = 892
        return size

    def calculateFinalHeader(self):
        finalHeader = array.array('B', telemetry.PrimaryHeader.build(dict(transfer_frame_version_number = self.transfer_frame_version_number,
                                                                          spacecraft_id = self.spacecraft_id,
                                                                          virtual_channel_id = self.virtual_channel_id,
                                                                          ocf_flag = self.ocf_flag,
                                                                          master_channel_frame_count = self.master_channel_frame_count,
                                                                          virtual_channel_frame_count = self.virtual_channel_frame_count,
                                                                          transfer_frame_secondary_header_flag = self.transfer_frame_secondary_header_flag,
                                                                          synch_flag = self.synch_flag,
                                                                          packet_order_flag = self.packet_order_flag,
                                                                          segment_length_id = self.segment_length_id,
                                                                          first_header_pointer = self.first_header_pointer)))
        return finalHeader
