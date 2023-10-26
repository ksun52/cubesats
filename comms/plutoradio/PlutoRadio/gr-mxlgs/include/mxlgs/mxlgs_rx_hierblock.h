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


#ifndef INCLUDED_MXLGS_MXLGS_RX_HIERBLOCK_H
#define INCLUDED_MXLGS_MXLGS_RX_HIERBLOCK_H

#include <mxlgs/api.h>
#include <gnuradio/hier_block2.h>

namespace gr {
  namespace mxlgs {

    /*!
     * \brief <+description of block+>
     * \ingroup mxlgs
     *
     */
    class MXLGS_API mxlgs_rx_hierblock : virtual public gr::hier_block2
    {
     public:
      typedef boost::shared_ptr<mxlgs_rx_hierblock> sptr;
      mxlgs_rx_hierblock();
      ~mxlgs_rx_hierblock();
      /*!
       * \brief Return a shared_ptr to a new instance of mxlgs::mxlgs_rx_hierblock.
       *
       * To avoid accidental use of raw pointers, mxlgs::mxlgs_rx_hierblock's
       * constructor is in a private implementation
       * class. mxlgs::mxlgs_rx_hierblock::make is the public interface for
       * creating new instances.
       */
      static sptr make();
    };

  } // namespace mxlgs
} // namespace gr

#endif /* INCLUDED_MXLGS_MXLGS_RX_HIERBLOCK_H */

