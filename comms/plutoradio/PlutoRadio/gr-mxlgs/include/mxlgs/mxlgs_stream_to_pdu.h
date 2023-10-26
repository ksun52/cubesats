/* -*- c++ -*- */
/*This program is written solely for the uses of MXL*/
/*Author: Srinagesh Sharma*/
/*
 * 
 * GNU Radio is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 * 
 * GNU Radio is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 * 
 * You should have received a copy of the GNU General Public License
 * along with GNU Radio; see the file COPYING.  If not, write to
 * the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#ifndef INCLUDED_MXLGS_STREAM_TO_PDU_H
#define INCLUDED_MXLGS_STREAM_TO_PDU_H

#undef VERBOSE

#include <mxlgs/api.h>
#include <gnuradio/sync_block.h>
#include <gnuradio/blocks/pdu.h>
#include <assert.h>

#define MAX_PACKET_LEN 16384
#define MIN_PACKET_LEN 17
#define FLAG 0x7E

class mxlgs_stream_to_pdu;
typedef boost::shared_ptr<mxlgs_stream_to_pdu> mxlgs_stream_to_pdu_sptr;

MXLGS_API mxlgs_stream_to_pdu_sptr mxlgs_make_stream_to_pdu (bool mode);

class MXLGS_API mxlgs_stream_to_pdu : public gr::sync_block
{
private:
	friend MXLGS_API mxlgs_stream_to_pdu_sptr mxlgs_make_stream_to_pdu (bool mode);
	mxlgs_stream_to_pdu (bool mode);

	enum state_t { STARTFLAG, PACKET, ENDFLAG, LASTFLAGBIT, END };
	state_t state;
	bool mode;
	unsigned char			sr,bitctr,ones,prevbit,bit,rbit;
  	unsigned int			bytectr,descr,flagctr, bytekissctr;
  	int d_signalstatus;

  	uint8_t				*pktbuf, *pktptr;
  	uint8_t				*pktkiss;
  	size_t				d_itemsize;
  	size_t 				d_pdu_length;
  	size_t				d_pdu_remain;
  	bool				d_inpdu;
  	gr::blocks::pdu::vector_type	d_type;
  	pmt::pmt_t			d_pdu_meta;
  	pmt::pmt_t 			d_pdu_vector;

public:
	int work (int noutput_items,
		    gr_vector_const_void_star &input_items,
		    gr_vector_void_star &output_items);
	void send_message();

};

#endif	/*INCLUDED_MXLGS_STREAM_TO_PDU_H*/
