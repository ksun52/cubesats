/* -*- c++ -*- */

#define MXLGS_API

%include "gnuradio.i"			// the common stuff
%import "constellation.i"       // the digital constellation swig
//%include "analog_swig.i"
//%include "filter_swig.i"
//%include "blocks_swig0.i"
//%include "blocks_swig1.i"
//%include "blocks_swig2.i"
//%include "blocks_swig3.i"
//%include "blocks_swig4.i"
//%include "blocks_swig5.i"

//load generated python docstrings
%include "mxlgs_swig_doc.i"

%{
#include "mxlgs/mxlgs_ax25_packetization.h"
#include "mxlgs/mxlgs_evmest_cf.h"
#include "mxlgs/mxlgs_stream_to_pdu.h"
#include "mxlgs/mxlgs_doppler_correction_cc.h"
%}

GR_SWIG_BLOCK_MAGIC(mxlgs, ax25_packetization);
%include "mxlgs/mxlgs_ax25_packetization.h"

GR_SWIG_BLOCK_MAGIC(mxlgs, evmest_cf);
%include "mxlgs/mxlgs_evmest_cf.h"

GR_SWIG_BLOCK_MAGIC(mxlgs, stream_to_pdu);
%include "mxlgs/mxlgs_stream_to_pdu.h"

GR_SWIG_BLOCK_MAGIC(mxlgs, doppler_correction_cc);
%include "mxlgs/mxlgs_doppler_correction_cc.h"

// %include "mxlgs/mxlgs_rx_hierblock.h"
// GR_SWIG_BLOCK_MAGIC2(mxlgs, mxlgs_rx_hierblock);
// 
// %include "mxlgs/mxlgs_tx_hierblock.h"
// GR_SWIG_BLOCK_MAGIC2(mxlgs, mxlgs_tx_hierblock);
