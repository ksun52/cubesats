/* -*- c++ -*- */
/* 
 * Copyright 2016 <+YOU OR YOUR COMPANY+>.
 * 
 * This is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option)
 * any later version.
 * 
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with this software; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 51 Franklin Street,
 * Boston, MA 02110-1301, USA.
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <vector>
#include <gnuradio/io_signature.h>
#include <mxlgs/mxlgs_rx_hierblock.h>
#include <gnuradio/blocks/add_const_cc.h>
#include <gnuradio/filter/fir_filter_ccf.h>
#include <gnuradio/filter/fir_filter_fff.h>
#include <mxlgs/mxlgs_doppler_correction_cc.h>
#include <gnuradio/filter/firdes.h>
#include <gnuradio/analog/quadrature_demod_cf.h>
#include <gnuradio/filter/rational_resampler_base_fff.h>
#include <gnuradio/digital/clock_recovery_mm_ff.h>
#include <gnuradio/digital/binary_slicer_fb.h>
#include <gnuradio/blocks/socket_pdu.h>
#include <gnuradio/filter/single_pole_iir_filter_ff.h>
#include <gnuradio/blocks/sub_ff.h>
#include <mxlgs/mxlgs_stream_to_pdu.h>
#include <math.h>

namespace gr {
  namespace mxlgs {

    mxlgs_rx_hierblock::sptr
    mxlgs_rx_hierblock::make()
    {
      return gnuradio::get_initial_sptr
        (new mxlgs_rx_hierblock());
    }

    /*
     * The private constructor
     */
    mxlgs_rx_hierblock::mxlgs_rx_hierblock()
      : gr::hier_block2("mxlgs_rx_hierblock",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {

      double bit_rate = 9600;
      double samp_rate = 256000;
      int unsigned I_interp = 3;
      int unsigned I_decim = 5;
      double resamp_rate = samp_rate*I_interp/I_decim;
      double bit_oversampling = resamp_rate/bit_rate;
      int unsigned port = 12800;
      int dir = 1;
      double int_freq = 50000;
      long int rxfreq = 437485000;
      double fmdev = 3000;
      double fmk = samp_rate/(2.0*M_PI*fmdev);
      double alpha = 0.0001;
      double mu = 0.5;
      double gain_mu = 0.05;


      std::vector<float> taps  = gr::filter::firdes::low_pass(1, samp_rate, 1.1*bit_rate, 4000, gr::filter::firdes::WIN_HANN);
      
      double fractional_bw = 0.4;
      double halfband = 0.5;
      double beta = 7.0;
      double rate = (double)I_interp/(double)I_decim;
      double trans_width;
      double mid_transition_band;
      if(rate >= 1.0)
      {
        trans_width = halfband - fractional_bw;
        mid_transition_band = rate*halfband - trans_width/2.0;
      }
      else
      {
        trans_width = rate*(halfband - fractional_bw);
        mid_transition_band = rate*halfband - trans_width/2.0;
      }


      std::vector<float> taps2 = gr::filter::firdes::low_pass(I_interp, I_interp, mid_transition_band, trans_width, gr::filter::firdes::WIN_KAISER, beta); // NEED TO FIND WHERE TO COMPUTE TAPS

      std::vector<float> taps3 = gr::filter::firdes::low_pass(1, resamp_rate, 0.7*bit_rate, 4000, gr::filter::firdes::WIN_HANN);


      gr::blocks::add_const_cc::sptr add_con(gr::blocks::add_const_cc::make(gr_complex(0,0)));

      mxlgs_doppler_correction_cc_sptr doppler_correction(mxlgs_make_doppler_correction_cc(samp_rate, port, dir, int_freq, rxfreq));

      gr::filter::fir_filter_ccf::sptr lowpass1(gr::filter::fir_filter_ccf::make(1, taps));

      gr::analog::quadrature_demod_cf::sptr demod(gr::analog::quadrature_demod_cf::make(fmk));

      gr::filter::single_pole_iir_filter_ff::sptr remove_dc(gr::filter::single_pole_iir_filter_ff::make(alpha, 1));

      gr::blocks::sub_ff::sptr sub1(gr::blocks::sub_ff::make(1));

      gr::filter::rational_resampler_base_fff::sptr resample(gr::filter::rational_resampler_base_fff::make(I_interp, I_decim, taps2));

      gr::filter::fir_filter_fff::sptr lowpass2(gr::filter::fir_filter_fff::make(1, taps3));

      gr::digital::clock_recovery_mm_ff::sptr clock_recovery(gr::digital::clock_recovery_mm_ff::make(bit_oversampling, 0.25*gain_mu*gain_mu, mu, gain_mu, 0.05));

      gr::digital::binary_slicer_fb::sptr slicer(gr::digital::binary_slicer_fb::make());

      mxlgs_stream_to_pdu_sptr stream_to_pdu(mxlgs_make_stream_to_pdu(true));

      gr::blocks::socket_pdu::sptr server(gr::blocks::socket_pdu::make("TCP_SERVER", "0.0.0.0", "12600"));

      // Connect input into doppler_correction
      connect(self(), 0, doppler_correction, 0);
      connect(doppler_correction, 0, lowpass1, 0);
      connect(lowpass1, 0, demod, 0);
      connect(demod, 0, remove_dc, 0);
      // Subtract two signals
      connect(demod, 0, sub1, 0);
      connect(remove_dc, 0, sub1, 1);

      connect(sub1, 0, resample, 0);
      connect(resample, 0, lowpass2, 0);
      connect(lowpass2, 0, clock_recovery, 0);
      connect(clock_recovery, 0, slicer, 0);
      connect(slicer, 0, stream_to_pdu, 0);
      msg_connect(stream_to_pdu, "pdus", server, "pdus");


      // Connect dopper corretion output to output of block for display on gui
      connect(doppler_correction , 0, self(), 0);

      
    }

    /*
     * Our virtual destructor.
     */
    mxlgs_rx_hierblock::~mxlgs_rx_hierblock()
    {
    }


  } /* namespace mxlgs */
} /* namespace gr */

