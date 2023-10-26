#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright 2018,2020 Daniel Estevez <daniel@destevez.net>
#
# This file is part of gr-satellites
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import datetime

from construct import *
import construct

from ..adapters import LinearAdapter

# See
# https://www.raumfahrttechnik.tu-berlin.de/fileadmin/fg169/
# amateur-radio/TUBiX10-COM.pdf
# for documentation

LTUFrameHeader = BitStruct(
    'SrcId' / BitsInteger(7),
    'DstId' / BitsInteger(7),
    'FrCntTx' / BitsInteger(4),
    'FrCntRx' / BitsInteger(4),
    'SNR' / BitsInteger(4),
    'AiTypeSrc' / BitsInteger(4),
    'AiTypeDst' / BitsInteger(4),
    'DfcId' / BitsInteger(2),
    'Caller' / Flag,
    'Arq' / Flag,
    'PduTypeId' / Flag,
    'BchRq' / Flag,
    'Hailing' / Flag,
    'UdFl1' / Flag,
    'PduLength' / BitsInteger(10),
    'CRC13' / BitsInteger(13),
    'CRC5' / BitsInteger(5),
    Padding(2)
    )


class TimeAdapter(Adapter):
    def _encode(self, obj, context, path=None):
        d = int((obj - datetime.datetime(2000, 1, 1))*2)
        return Container(
            days=d.days,
            milliseconds=d.seconds * 1000 + d.microseconds / 1000)

    def _decode(self, obj, context, path=None):
        return (datetime.datetime(2000, 1, 1)
                + datetime.timedelta(seconds=float(obj)/2.0))


TimeStamp = TimeAdapter(BitsInteger(32, swapped=True))


SNETFrameHeaderExtension = BitStruct(
    'VersNo' / BitsInteger(2),
    'DFCID' / BitsInteger(2),
    'ExtensionRFU' / BitsInteger(4),
    'ChannelInfo' / BitsInteger(8),
    'QoS' / Flag,
    'PDUTypeID' / Flag,
    'ARQ' / Flag,
    'ControlRFU' / BitsInteger(5),
    'TimeTagSub' / BitsInteger(16),
    'SCID' / BitsInteger(10),
    'SeqNo' / BitsInteger(14)
    )

SNETFrameHeader = BitStruct(
    Const(0b111100110101000000, BitsInteger(18)),
    'CRC' / BitsInteger(14),
    'FCIDMajor' / BitsInteger(6),
    'FCIDSub' / BitsInteger(10),
    'Urgent' / Flag,
    'Extended' / Flag,
    'CheckCRC' / Flag,
    'Multiframe' / Flag,
    'TimeTaggedSetting' / Flag,
    'TimeTagged' / Flag,
    'DataLength' / BitsInteger(10),
    'TimeTag' / If(lambda c: c.TimeTagged, TimeStamp),
    'Extension' / If(lambda c: c.Extended, SNETFrameHeaderExtension)
    )

Battery = Struct(
    'V_BAT' / LinearAdapter(2, Int16sl),
    'A_IN_CHARGER' / LinearAdapter(12, Int16sl),
    'A_OUT_CHARGER' / LinearAdapter(6, Int16sl)
    )

BatteryCurrents = Struct(
    'A_IN' / LinearAdapter(12, Int16sl),
    'A_OUT' / LinearAdapter(12, Int16sl)
    )

EPSTelemetry = Struct(
    'CUR_SOL' / LinearAdapter(50, Int16sl)[6],
    'V_SOL' / Int16sl,
    'BATTERIES' / Battery[2],
    'V_SUM' / LinearAdapter(2, Int16sl),
    'V_3V3' / LinearAdapter(8, Int16sl),
    'V_5V' / LinearAdapter(5, Int16sl),
    'TEMP_BATT' / LinearAdapter(256, Int16sl)[2],
    'TEMP_OBC' / Int16sl,
    'A_OBC' / Int16ul,
    'V_OBC' / Int16ul,
    'BATT_CURRENTS' / BatteryCurrents[2]
    )

ADCSFlags = BitStruct(
    Padding(4),
    'AttDetTrackIGRFDeltaB' / Flag,
    'AttDetSuseAlbedoTracking' / Flag,
    'SUSE1AlbedoFlag' / Flag,
    'SUSE2AlbedoFlag' / Flag,
    'SUSE3AlbedoFlag' / Flag,
    'SUSE4AlbedoFlag' / Flag,
    'SUSE5AlbedoFlag' / Flag,
    'SUSE6AlbedoFlag' / Flag,
    'AttDetAutoVirtualizeMFSA' / Flag,
    'AttDetAutoVirtualizeSUSEA' / Flag,
    'AttDetNarrowVectors' / Flag,
    'AttDetMismatchingVectors' / Flag
)

ADCSTelemetry = Struct(
    'iModeChkListThisStepActive' / Int8sl,
    'iAttDetFinalState' / Int8ul,
    'iSensorArrayAvailStatusGA' / Int8ul,
    'iSensorArrayAvailStatusMFSA' / Int8ul,
    'iSensorArrayAvailStatusSUSEA' / Int8ul,
    'iActArrayAvailStatusRWA' / Int8ul,
    'iActArrayAvailStatusMATA' / Int8ul,
    'AttDetMfsDistCorrMode' / Int8ul,
    'AttDetSuseDistCorrMode' / Int8ul,
    'flags' / ADCSFlags,
    'omegaXOptimal_SAT' / LinearAdapter(260, Int16sl),
    'omegaYOptimal_SAT' / LinearAdapter(260, Int16sl),
    'omegaZOptimal_SAT' / LinearAdapter(260, Int16sl),
    'magXOptimal_SAT' / LinearAdapter(0.1, Int16sl),
    'magYOptimal_SAT' / LinearAdapter(0.1, Int16sl),
    'magZOptimal_SAT' / LinearAdapter(0.1, Int16sl),
    'sunXOptimal_SAT' / LinearAdapter(32000, Int16sl),
    'sunYOptimal_SAT' / LinearAdapter(32000, Int16sl),
    'sunZOptimal_SAT' / LinearAdapter(32000, Int16sl),
    'dCtrlTorqueRWAx_SAT_lr' / LinearAdapter(38484, Int8ul),
    'dCtrlTorqueRWAy_SAT_lr' / LinearAdapter(38484, Int8ul),
    'dCtrlTorqueRWAz_SAT_lr' / LinearAdapter(38484, Int8ul),
    'dCtrlMagMomentMATAx_SAT_lr' / LinearAdapter(127, Int8ul),
    'dCtrlMagMomentMATAy_SAT_lr' / LinearAdapter(127, Int8ul),
    'dCtrlMagMomentMATAz_SAT_lr' / LinearAdapter(127, Int8ul),
    'iReadTorqueRWx_MFR' / LinearAdapter(9696969, Int16ul),
    'iReadTorqueRWy_MFR' / LinearAdapter(9696969, Int16ul),
    'iReadTorqueRWz_MFR' / LinearAdapter(9696969, Int16ul),
    'iReadRotSpeedRWx_MFR' / Int16ul,
    'iReadRotSpeedRWy_MFR' / Int16ul,
    'iReadRotSpeedRWz_MFR' / Int16ul,
    'SGP4LatXPEF' / LinearAdapter(355, Int16ul),
    'SGP4LongYPEF' / LinearAdapter(177, Int16ul),
    'SGP4AltPEF' / LinearAdapter(0.25, Int8ul),
    'AttitudeErrorAngle' / LinearAdapter(177, Int16ul),
    'TargetData_Distance' / Int16ul,
    'TargetData_ControlIsActive' / Int8ul  # flag, really
    )


snet = Struct(
    'header' / SNETFrameHeader,
    'telemetry' / Switch(lambda c: (c.header.FCIDMajor, c.header.FCIDSub), {
        (0, 0): ADCSTelemetry,
        (9, 0): EPSTelemetry,
    }, default=Pass))
