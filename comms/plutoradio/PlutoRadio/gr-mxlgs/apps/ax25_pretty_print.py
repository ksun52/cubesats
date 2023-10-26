"""
Embedded Python Blocks:q

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import hexdump


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='AX.25 Pretty Print',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message_port_register_in(pmt.intern('pdu'))
        self.set_msg_handler(pmt.intern('pdu'), self.handle_msg)

    def handle_msg(self, msg_pmt):
        msg = pmt.cdr(msg_pmt)
        packet = bytearray(pmt.u8vector_elements(msg))
        
        if len(packet) < 14:
            print('[AX.25 Pretty Print] Err: received packet that is too short for AX.25 (<14 bytes)')
            return
        dst = bytearray([x >> 1 for x in packet[0:7]]).decode()[0:-1]
        src = bytearray([x >> 1 for x in packet[7:14]]).decode()[0:-1]
        data = packet[14:]
        print('')
        print('{}->{} | {} bytes'.format(src, dst, len(data)))
        hexdump.hexdump(bytes(data))
        print('')


