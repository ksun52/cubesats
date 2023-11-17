
/*
 * This file was automatically generated using swig_doc.py.
 *
 * Any changes to it will be lost next time it is regenerated.
 */






%feature("docstring") mxlgs_ax25_packetization::mxlgs_ax25_packetization "

Params: (start_tx_delay, end_tx_delay, bit_oversampling, interp, decim)"

%feature("docstring") mxlgs_ax25_packetization::~mxlgs_ax25_packetization "

Params: (NONE)"

%feature("docstring") mxlgs_ax25_packetization::current_tags "

Params: (NONE)"

%feature("docstring") mxlgs_ax25_packetization::set_display "

Params: (d)"

%feature("docstring") mxlgs_ax25_packetization::make_packet "

Params: (pktarray, pktbufkiss)"

%feature("docstring") mxlgs_ax25_packetization::general_work "

Params: (noutput_items, ninput_items, input_items, output_items)"

%feature("docstring") mxlgs_make_ax25_packetization "

Params: (start_tx_delay, end_tx_delay, bit_oversampling, interp, decim)"



%feature("docstring") mxlgs_doppler_correction_cc::mxlgs_doppler_correction_cc "

Params: (sampling_freq, port, dir, int_freq, rxfreq)"

%feature("docstring") mxlgs_doppler_correction_cc::start_thread "

Params: (obj)"

%feature("docstring") mxlgs_doppler_correction_cc::~mxlgs_doppler_correction_cc "

Params: (NONE)"

%feature("docstring") mxlgs_doppler_correction_cc::socket_thread_work "

Params: (NONE)"

%feature("docstring") mxlgs_doppler_correction_cc::process_command "

Params: (, )"

%feature("docstring") mxlgs_doppler_correction_cc::work "

Params: (noutput_items, input_items, output_items)"

%feature("docstring") mxlgs_make_doppler_correction_cc "

Params: (sampling_freq, port, dir, int_freq, rxfreq)"



%feature("docstring") mxlgs_evmest_cf::mxlgs_evmest_cf "

Params: (npoints, lvec, cnst)"

%feature("docstring") mxlgs_evmest_cf::~mxlgs_evmest_cf "

Params: (NONE)"

%feature("docstring") mxlgs_evmest_cf::work "

Params: (noutput_items, input_items, output_items)"

%feature("docstring") mxlgs_make_evmest_cf "

Params: (npoints, lvec, cnst)"



%feature("docstring") mxlgs_stream_to_pdu::mxlgs_stream_to_pdu "

Params: (mode)"

%feature("docstring") mxlgs_stream_to_pdu::work "

Params: (noutput_items, input_items, output_items)"

%feature("docstring") mxlgs_stream_to_pdu::send_message "

Params: (NONE)"

%feature("docstring") mxlgs_make_stream_to_pdu "

Params: (mode)"

%feature("docstring") gr::mxlgs::mxlgs_rx_hierblock "<+description of block+>"

%feature("docstring") gr::mxlgs::mxlgs_rx_hierblock::mxlgs_rx_hierblock "

Params: (NONE)"

%feature("docstring") gr::mxlgs::mxlgs_rx_hierblock::~mxlgs_rx_hierblock "

Params: (NONE)"

%feature("docstring") gr::mxlgs::mxlgs_rx_hierblock::make "Return a shared_ptr to a new instance of mxlgs::mxlgs_rx_hierblock.

To avoid accidental use of raw pointers, mxlgs::mxlgs_rx_hierblock's constructor is in a private implementation class. mxlgs::mxlgs_rx_hierblock::make is the public interface for creating new instances.

Params: (NONE)"

%feature("docstring") gr::mxlgs::mxlgs_tx_hierblock "<+description of block+>"

%feature("docstring") gr::mxlgs::mxlgs_tx_hierblock::make "Return a shared_ptr to a new instance of mxlgs::mxlgs_tx_hierblock.

To avoid accidental use of raw pointers, mxlgs::mxlgs_tx_hierblock's constructor is in a private implementation class. mxlgs::mxlgs_tx_hierblock::make is the public interface for creating new instances.

Params: (NONE)"