#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018-2019 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

from construct import *

from ..adapters import UNIXTimestampAdapter
from .csp import CSPHeader


Timestamp = UNIXTimestampAdapter(Int32ub)

Beacon0EPS = Struct(
    'timestamp' / Timestamp,
    'pv_v' / Int16ub[3],
    'batt_v' / Int16ub,
    'output_cur' / Int16ub[7],
    'pv_cur' / Int16ub[3],
    'batt_in_cur' / Int16ub,
    'batt_out_cur' / Int16ub,
    'temp' / Int16ub[6],
    'batt_mode' / Int8ub
    )

Beacon0COM = Struct(
    'timestamp' / Timestamp,
    'temp' / Int16sb[2],
    'rssi' / Int16sb,
    'rferr' / Int16sb,
    'rssi_bgnd' / Int16sb
    )

Beacon0OBC = Struct(
    'timestamp' / Timestamp,
    'cur' / Int16ub[6],
    'temp' / Int16sb[2]
    )

Beacon0 = Struct(
    'beacon_type' / Const(b'\x00'),
    'eps' / Beacon0EPS,
    'com' / Beacon0COM,
    'obc' / Beacon0OBC
    )

Beacon1EPS = Struct(
    'timestamp' / Timestamp,
    'wdt_i2c' / Int32ub,
    'wdt_gnd' / Int32ub,
    'boot_count' / Int32ub,
    'wdt_i2c_count' / Int32ub,
    'wdt_gnd_count' / Int32ub,
    'wdt_csp_count' / Int32ub[2],
    'wdt_csp' / Int8ub[2],
    'boot_cause' / Int8ub,
    'latchup' / Int16ub[6],
    'out_val' / Int8ub[8],
    'ppt_mode' / Int8ub
    )

Beacon1COM = Struct(
    'timestamp' / Timestamp,
    'tx_duty' / Int8ub,
    'total_tx_count' / Int32ub,
    'total_rx_count' / Int32ub,
    'total_tx_bytes' / Int32ub,
    'total_rx_bytes' / Int32ub,
    'boot_count' / Int16ub,
    'boot_cause' / Int32ub,
    'tx_bytes' / Int32ub,
    'rx_bytes' / Int32ub,
    'config' / Int8ub,
    'tx_count' / Int32ub,
    'rx_count' / Int32ub
    )

Beacon1OBC = Struct(
    'timestamp' / Timestamp,
    'pwr' / Int8ub[6],
    'sw_count' / Int16ub,
    'filesystem' / Int8ub,
    'boot_count' / Int16ub,
    'boot_cause' / Int32ub,
    'clock' / Timestamp
    )

Beacon1 = Struct(
    'beacon_type' / Const(b'\x01'),
    'eps' / Beacon1EPS,
    'com' / Beacon1COM,
    'obc' / Beacon1OBC
    )

suomi100 = Struct(
    'header' / CSPHeader,
    'payload' / Select(Beacon0, Beacon1)
    )
