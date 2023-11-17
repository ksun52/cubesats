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

#include <gnuradio/io_signature.h>
#include <mxlgs/mxlgs_tx_hierblock.h>

namespace gr {
  namespace mxlgs {

    mxlgs_tx_hierblock::sptr
    mxlgs_tx_hierblock::make()
    {
      return gnuradio::get_initial_sptr
        (new mxlgs_tx_hierblock());
    }

    /*
     * The private constructor
     */
    mxlgs_tx_hierblock::mxlgs_tx_hierblock()
      : gr::hier_block2("mxlgs_tx_hierblock",
              gr::io_signature::make(1, 1, sizeof(gr_complex)),
              gr::io_signature::make(1, 1, sizeof(gr_complex)))
    {
        connect(self(), 0, d_firstblock, 0);
        // connect other blocks
        connect(d_lastblock, 0, self(), 0);
    }

    /*
     * Our virtual destructor.
     */
    mxlgs_tx_hierblock_impl::~mxlgs_tx_hierblock_impl()
    {
    }


  } /* namespace mxlgs */
} /* namespace gr */

