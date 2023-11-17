#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: CFLh
# Author: MXL
# Description: MXL Ground Station System - Default Frequency 437.1 MHz
# Generated: Wed Mar 16 16:06:56 2022
##################################################


import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from datetime import datetime
from demod_gfsk_g3ruh import demod_gfsk_g3ruh  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import iio
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from numpy import array, convolve
from optparse import OptionParser
import math
import mxlgs
import numpy
import satellites


class CFLh(gr.top_block):

    def __init__(self, I_decimation=5, I_interpolation=3, TCP_host="172.16.1.44", TCP_port="12600", beacon_size=10, bit_rate=9600*1, intFreq=0, rxdevice_addr="serial=31C03D7", rxfreq=437.2e6, rxgain=10, samp_rate=128000*10, tx_delay=99, txdevice_addr="serial=31C03D7", txfmdev=10000, txfreq=437.2e6, txgain=30):
        gr.top_block.__init__(self, "CFLh")

        ##################################################
        # Parameters
        ##################################################
        self.I_decimation = I_decimation
        self.I_interpolation = I_interpolation
        self.TCP_host = TCP_host
        self.TCP_port = TCP_port
        self.beacon_size = beacon_size
        self.bit_rate = bit_rate
        self.intFreq = intFreq
        self.rxdevice_addr = rxdevice_addr
        self.rxfreq = rxfreq
        self.rxgain = rxgain
        self.samp_rate = samp_rate
        self.tx_delay = tx_delay
        self.txdevice_addr = txdevice_addr
        self.txfmdev = txfmdev
        self.txfreq = txfreq
        self.txgain = txgain

        ##################################################
        # Variables
        ##################################################
        self.resamp_rate = resamp_rate = samp_rate*I_interpolation/I_decimation
        self.buffer_fraction = buffer_fraction = 20
        self.bit_oversampling = bit_oversampling = resamp_rate/bit_rate
        self.sqwave = sqwave = (1,)*(resamp_rate/bit_rate)
        self.gaussian_taps = gaussian_taps = firdes.gaussian(1, bit_oversampling, 1, 4*bit_oversampling)
        self.default_buffer_size = default_buffer_size = math.pow(2,15)
        self.buffer_size = buffer_size = (41+tx_delay+beacon_size)*8*bit_oversampling*I_decimation/I_interpolation/buffer_fraction

        ##################################################
        # Blocks
        ##################################################
        self.satellites_print_timestamp_0_0 = satellites.print_timestamp('%Y-%m-%d %H:%M:%S', True)
        self.satellites_pdu_to_kiss_0 = satellites.pdu_to_kiss()
        self.satellites_hdlc_deframer_0 = satellites.hdlc_deframer(check_fcs=True, max_length=10000)
        self.rational_resampler_xxx_0 = filter.rational_resampler_fff(
                interpolation=I_decimation,
                decimation=I_interpolation,
                taps=(filter.design_filter(I_decimation, I_interpolation,0.4)),
                fractional_bw=None,
        )
        self.plutoSDR_sink = iio.pluto_sink('ip:192.168.2.1', int(txfreq+int(intFreq)), int(samp_rate), int(samp_rate), buffer_size, False, 0, '', True)
        self.mxlgs_doppler_correction_cc_1 = mxlgs.doppler_correction_cc(samp_rate, 12900, -1, -int(intFreq), int(txfreq))
        self.mxlgs_doppler_correction_cc_0 = mxlgs.doppler_correction_cc(samp_rate, 12800, 1, int(intFreq), int(rxfreq))
        self.mxlgs_ax25_packetization_0 = mxlgs.ax25_packetization(tx_delay, 5, bit_oversampling, I_decimation, I_interpolation)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(resamp_rate/bit_rate, (convolve(array(gaussian_taps),array(sqwave))))
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.demod_gfsk_g3ruh_0 = demod_gfsk_g3ruh(
            baud_rate=9600,
            bit_avg=60,
            fsk_deviation=3000,
            samp_per_sym=5,
            samp_rate=samp_rate,
        )
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", '0.0.0.0', '12600', 10000, False)
        (self.blocks_socket_pdu_0).set_min_output_buffer(100)
        (self.blocks_socket_pdu_0).set_max_output_buffer(100)
        self.blocks_pdu_to_tagged_stream_0 = blocks.pdu_to_tagged_stream(blocks.byte_t, 'packet_len')
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((1, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vff((-0.5, ))
        self.analog_frequency_modulator_fc_0 = analog.frequency_modulator_fc(2*math.pi*txfmdev/(samp_rate))



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.blocks_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.satellites_hdlc_deframer_0, 'out'), (self.satellites_print_timestamp_0_0, 'in'))
        self.msg_connect((self.satellites_pdu_to_kiss_0, 'out'), (self.blocks_socket_pdu_0, 'pdus'))
        self.msg_connect((self.satellites_print_timestamp_0_0, 'out'), (self.satellites_pdu_to_kiss_0, 'in'))
        self.connect((self.analog_frequency_modulator_fc_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.mxlgs_doppler_correction_cc_1, 0))
        self.connect((self.blocks_null_source_0, 0), (self.mxlgs_doppler_correction_cc_0, 0))
        self.connect((self.blocks_pdu_to_tagged_stream_0, 0), (self.mxlgs_ax25_packetization_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.demod_gfsk_g3ruh_0, 0), (self.satellites_hdlc_deframer_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.mxlgs_ax25_packetization_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.mxlgs_doppler_correction_cc_0, 0), (self.demod_gfsk_g3ruh_0, 0))
        self.connect((self.mxlgs_doppler_correction_cc_1, 0), (self.plutoSDR_sink, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_frequency_modulator_fc_0, 0))

    def get_I_decimation(self):
        return self.I_decimation

    def set_I_decimation(self, I_decimation):
        self.I_decimation = I_decimation
        self.set_resamp_rate(self.samp_rate*self.I_interpolation/self.I_decimation)
        self.set_buffer_size((41+self.tx_delay+self.beacon_size)*8*self.bit_oversampling*self.I_decimation/self.I_interpolation/self.buffer_fraction)
        self.rational_resampler_xxx_0.set_taps((filter.design_filter(self.I_decimation, self.I_interpolation,0.4)))

    def get_I_interpolation(self):
        return self.I_interpolation

    def set_I_interpolation(self, I_interpolation):
        self.I_interpolation = I_interpolation
        self.set_resamp_rate(self.samp_rate*self.I_interpolation/self.I_decimation)
        self.set_buffer_size((41+self.tx_delay+self.beacon_size)*8*self.bit_oversampling*self.I_decimation/self.I_interpolation/self.buffer_fraction)
        self.rational_resampler_xxx_0.set_taps((filter.design_filter(self.I_decimation, self.I_interpolation,0.4)))

    def get_TCP_host(self):
        return self.TCP_host

    def set_TCP_host(self, TCP_host):
        self.TCP_host = TCP_host

    def get_TCP_port(self):
        return self.TCP_port

    def set_TCP_port(self, TCP_port):
        self.TCP_port = TCP_port

    def get_beacon_size(self):
        return self.beacon_size

    def set_beacon_size(self, beacon_size):
        self.beacon_size = beacon_size
        self.set_buffer_size((41+self.tx_delay+self.beacon_size)*8*self.bit_oversampling*self.I_decimation/self.I_interpolation/self.buffer_fraction)

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate
        self.set_sqwave((1,)*(self.resamp_rate/self.bit_rate))
        self.set_bit_oversampling(self.resamp_rate/self.bit_rate)

    def get_intFreq(self):
        return self.intFreq

    def set_intFreq(self, intFreq):
        self.intFreq = intFreq
        self.plutoSDR_sink.set_params(int(self.txfreq+int(self.intFreq)), int(self.samp_rate), int(self.samp_rate), 38, '', True)

    def get_rxdevice_addr(self):
        return self.rxdevice_addr

    def set_rxdevice_addr(self, rxdevice_addr):
        self.rxdevice_addr = rxdevice_addr

    def get_rxfreq(self):
        return self.rxfreq

    def set_rxfreq(self, rxfreq):
        self.rxfreq = rxfreq

    def get_rxgain(self):
        return self.rxgain

    def set_rxgain(self, rxgain):
        self.rxgain = rxgain

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_resamp_rate(self.samp_rate*self.I_interpolation/self.I_decimation)
        self.plutoSDR_sink.set_params(int(self.txfreq+int(self.intFreq)), int(self.samp_rate), int(self.samp_rate), 38, '', True)
        self.demod_gfsk_g3ruh_0.set_samp_rate(self.samp_rate)
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*math.pi*self.txfmdev/(self.samp_rate))

    def get_tx_delay(self):
        return self.tx_delay

    def set_tx_delay(self, tx_delay):
        self.tx_delay = tx_delay
        self.set_buffer_size((41+self.tx_delay+self.beacon_size)*8*self.bit_oversampling*self.I_decimation/self.I_interpolation/self.buffer_fraction)

    def get_txdevice_addr(self):
        return self.txdevice_addr

    def set_txdevice_addr(self, txdevice_addr):
        self.txdevice_addr = txdevice_addr

    def get_txfmdev(self):
        return self.txfmdev

    def set_txfmdev(self, txfmdev):
        self.txfmdev = txfmdev
        self.analog_frequency_modulator_fc_0.set_sensitivity(2*math.pi*self.txfmdev/(self.samp_rate))

    def get_txfreq(self):
        return self.txfreq

    def set_txfreq(self, txfreq):
        self.txfreq = txfreq
        self.plutoSDR_sink.set_params(int(self.txfreq+int(self.intFreq)), int(self.samp_rate), int(self.samp_rate), 38, '', True)

    def get_txgain(self):
        return self.txgain

    def set_txgain(self, txgain):
        self.txgain = txgain

    def get_resamp_rate(self):
        return self.resamp_rate

    def set_resamp_rate(self, resamp_rate):
        self.resamp_rate = resamp_rate
        self.set_sqwave((1,)*(self.resamp_rate/self.bit_rate))
        self.set_bit_oversampling(self.resamp_rate/self.bit_rate)

    def get_buffer_fraction(self):
        return self.buffer_fraction

    def set_buffer_fraction(self, buffer_fraction):
        self.buffer_fraction = buffer_fraction
        self.set_buffer_size((41+self.tx_delay+self.beacon_size)*8*self.bit_oversampling*self.I_decimation/self.I_interpolation/self.buffer_fraction)

    def get_bit_oversampling(self):
        return self.bit_oversampling

    def set_bit_oversampling(self, bit_oversampling):
        self.bit_oversampling = bit_oversampling
        self.set_gaussian_taps(firdes.gaussian(1, self.bit_oversampling, 1, 4*self.bit_oversampling))
        self.set_buffer_size((41+self.tx_delay+self.beacon_size)*8*self.bit_oversampling*self.I_decimation/self.I_interpolation/self.buffer_fraction)

    def get_sqwave(self):
        return self.sqwave

    def set_sqwave(self, sqwave):
        self.sqwave = sqwave
        self.interp_fir_filter_xxx_0.set_taps((convolve(array(self.gaussian_taps),array(self.sqwave))))

    def get_gaussian_taps(self):
        return self.gaussian_taps

    def set_gaussian_taps(self, gaussian_taps):
        self.gaussian_taps = gaussian_taps
        self.interp_fir_filter_xxx_0.set_taps((convolve(array(self.gaussian_taps),array(self.sqwave))))

    def get_default_buffer_size(self):
        return self.default_buffer_size

    def set_default_buffer_size(self, default_buffer_size):
        self.default_buffer_size = default_buffer_size

    def get_buffer_size(self):
        return self.buffer_size

    def set_buffer_size(self, buffer_size):
        self.buffer_size = buffer_size


def argument_parser():
    description = 'MXL Ground Station System - Default Frequency 437.1 MHz'
    parser = OptionParser(usage="%prog: [options]", option_class=eng_option, description=description)
    parser.add_option(
        "", "--TCP-port", dest="TCP_port", type="string", default="12600",
        help="Set TCP_port [default=%default]")
    parser.add_option(
        "", "--rxdevice-addr", dest="rxdevice_addr", type="string", default="serial=31C03D7",
        help="Set rxdevice_addr [default=%default]")
    parser.add_option(
        "", "--txdevice-addr", dest="txdevice_addr", type="string", default="serial=31C03D7",
        help="Set txdevice_addr [default=%default]")
    return parser


def main(top_block_cls=CFLh, options=None):
    if options is None:
        options, _ = argument_parser().parse_args()

    tb = top_block_cls(TCP_port=options.TCP_port, rxdevice_addr=options.rxdevice_addr, txdevice_addr=options.txdevice_addr)
    tb.start()
    try:
        raw_input('Press Enter to quit: ')
    except EOFError:
        pass
    tb.stop()
    tb.wait()


if __name__ == '__main__':
    main()
