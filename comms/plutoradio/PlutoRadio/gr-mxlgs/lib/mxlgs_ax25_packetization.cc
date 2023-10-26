/* -*- c++ -*- */
/*Michigan eXploration Labs*/
/*Author: Srinagesh Sharma*/
/*
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

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <mxlgs/mxlgs_ax25_packetization.h>
#include <gnuradio/io_signature.h>
#include <gnuradio/blocks/pdu.h>
#include <gnuradio/thread/thread.h>
#include <iostream>
#include <iomanip>

#define KISS_FEND 0XC0
#define KISS_FESC 0XDB
#define KISS_TFEND 0xDC
#define KISS_TFESC 0xDD

#undef VERBOSE

/*-------------------------------------
 *			SHARED PTR
 *------------------------------------*/
mxlgs_ax25_packetization_sptr mxlgs_make_ax25_packetization(unsigned int start_tx_delay, unsigned int end_tx_delay, float bit_oversampling, float interp, float decim)
{
	return mxlgs_ax25_packetization_sptr (new mxlgs_ax25_packetization(start_tx_delay, end_tx_delay, bit_oversampling, interp, decim));
}

/*-------------------------------------
 *			CONSTRUCTOR
 *------------------------------------*/
mxlgs_ax25_packetization::mxlgs_ax25_packetization(unsigned int start_tx_delay, unsigned int end_tx_delay, float bit_oversampling, float interp, float decim)
	:gr::block ("AX25_packetization",
		gr::io_signature::make(1,1,sizeof(unsigned char)),
		gr::io_signature::make(1,1,sizeof(unsigned char))),
	d_display(true), d_start_tx_delay(start_tx_delay), d_end_tx_delay(end_tx_delay), d_bit_oversampling(bit_oversampling), d_interp(interp), d_decim(decim) 
	{
    control = 0x03;
    pid = 0xF0;

    // GRIFEX EDU (Geo)
    dest_id = (unsigned char *)"CQ";
    dest_length = 2;
    source_id = (unsigned char *)"KD8SPS";
    source_length = 6;

    // TBEX EDU (Ted)
    dest_id = (unsigned char *)"KD8SPS";
    dest_length = 6;
    source_id = (unsigned char *)"CQ";
    source_length = 2;

    dest_id = (unsigned char *)"KF6RFX";
    dest_length = 6;
    source_id = (unsigned char *)"KD8SPS";
    source_length = 6;

    /*
    dest_id = (unsigned char *)"KD8SPS";
    dest_length = 6;
    source_id = (unsigned char *)"KF6RFX";
    source_length = 6;
    */



    pktbuf = new uint8_t [MAX_PACKET_LEN];
    pktbufkiss = new uint8_t [MAX_PACKET_LEN];
    pktarray = new uint8_t [MAX_PACKET_LEN + d_start_tx_delay + d_end_tx_delay];
    // enable_update_rate(true);
    noutput_cnt = 0;
}

/*-------------------------------------
 *			DESTRUCTOR
 *------------------------------------*/
mxlgs_ax25_packetization::~mxlgs_ax25_packetization()
{}

std::vector<gr::tag_t>
    mxlgs_ax25_packetization::current_tags()
    {
      gr::thread::scoped_lock l(d_mutex);
      return d_tags;
    }

void
    mxlgs_ax25_packetization::set_display(bool d)
    {
      gr::thread::scoped_lock l(d_mutex);
      d_display = d;
    }

static unsigned char nrzi(unsigned char x){
 static unsigned char r = 1;

  if(x == 0){
    r = (~r) & 0x1;
  }

  return r;
}

static unsigned char scramble(unsigned char x){
  static unsigned int shiftreg = 0;
  unsigned char y;

  y = x ^ ((shiftreg>>11)&1) ^ ((shiftreg>>16)&1);
  shiftreg = (shiftreg<<1)|y;

  return y;
}


void mxlgs_ax25_packetization::make_packet(unsigned char *pktarray, unsigned char *pktbufkiss)
{
  fcshi = 0xFF;
  fcslo = 0xFF;

  pkt_len = 0;

  for (uint64_t i = 0; i < d_start_tx_delay; i++)
  {
    if(i<3*d_start_tx_delay/4)
      pktarray[i] = 0xAA;
    else
      pktarray[i] = FLAG;
  }

  pkt_len = d_start_tx_delay;

  //Add the Destination, Source, Control, PID
  for (int i = 0; i < 6; i++)
  {
    if (i >= dest_length)
      pktarray[pkt_len + i] = 0x40;
    else
      pktarray[pkt_len + i] = (dest_id[i] << 1);
  }
  pkt_len = pkt_len + 6;

  pktarray[pkt_len] = 0x60;
  pkt_len++;

  for (int i = 0; i < 6; i++)
  {
    if (i >= source_length)
      pktarray[pkt_len + i] = 0x40;
    else
      pktarray[pkt_len + i] = (source_id[i] << 1);
  }
  pkt_len = pkt_len + 6;

  pktarray[pkt_len] = 0x61;
  pkt_len = pkt_len + 1;

  pktarray[pkt_len] = control;
  pkt_len++;

  pktarray[pkt_len] = pid;
  pkt_len++;

  //Add the input bytes

  for (int i = 0; i < input_pkt_lenkiss; i++)
  {
    pktarray[pkt_len + i] = pktbufkiss[i];
  }
  pkt_len = pkt_len + input_pkt_lenkiss;

  //Compute and add the Frame Check Sequence to the packet
  for (int i = d_start_tx_delay; i < pkt_len; ++i)
  {
      for(int j = 0; j < 8; j++){
      unsigned char cur_bit = (pktarray[i] & (1<<j)) ? 1 : 0;
      unsigned char b1 = fcshi & 0x01;
      unsigned char b2 = fcslo & 0x01;
      fcshi >>= 1;
      fcslo >>= 1;
      fcslo |= (b1<<7);
      if(b2 != cur_bit){
        fcshi = fcshi ^ 0x84;
        fcslo = fcslo ^ 0x08;
      }
    }
  }

  pktarray[pkt_len] = (fcslo ^ 0xFF);
  pktarray[pkt_len+1] = (fcshi ^ 0xFF);
  pkt_len = pkt_len + 2;

  for (int i = 0; i< d_end_tx_delay;i++)
  {
    pktarray[pkt_len+i] = FLAG;
  }
  pkt_len = pkt_len + d_end_tx_delay;

}

/*-------------------------------------
 *			WORK FUNCTION
 *------------------------------------*/
int mxlgs_ax25_packetization::general_work(int noutput_items,
    gr_vector_int &ninput_items,
		gr_vector_const_void_star &input_items,
		gr_vector_void_star &output_items)
{
	gr::thread::scoped_lock l(d_mutex);
	const unsigned char *in = (const unsigned char *) input_items[0];
  unsigned char *out = (unsigned char *) output_items[0];
  const int *ninput = (const int *) ninput_items[0];

      std::stringstream sout;
      if(d_display) {
        sout << std::endl
             << "----------------------------------------------------------------------";
        sout << std::endl << "Tag Debug: " << d_name << std::endl;
      }

      uint64_t abs_N, end_N;
      uint64_t tagoffset;

      noutput_cnt = 0;

      for(size_t i = 0; i < input_items.size(); i++) {
        abs_N = nitems_read(i);
        end_N = abs_N + (uint64_t)(noutput_items);

        d_tags.clear();
        get_tags_in_range(d_tags, i, abs_N, end_N);

        
    		d_tags_itr = d_tags.begin();
    		/*	sout << std::setw(10) << "Offset: " << d_tags_itr->offset
    			 << std::setw(10) << "Source: " 
    			 << (pmt::pmt_is_symbol(d_tags_itr->srcid) ? pmt::pmt_symbol_to_string(d_tags_itr->srcid) : "n/a")
    			 << std::setw(10) << "Key: " << pmt::pmt_symbol_to_string(d_tags_itr->key)
    			 << std::setw(10) << "Value: ";
    			sout << d_tags_itr->value << std::endl;
    		*/

          // sout << d_tags.size() << std::endl;
          // sout << d_tags_itr->key << std::endl;
          // sout << d_tags_itr->value << std::endl;

    			//start from the tag offset value and copy and print only the packet.
    			tagoffset = (d_tags_itr->offset) - abs_N;
          input_pkt_len = pmt::to_uint64(d_tags_itr->value);
    			for(uint64_t j=0; j<input_pkt_len;j++){
    				pktbuf[j] = in[tagoffset+j];
    				sout<<" "<<std::hex<<(int)pktbuf[j];
    			}
    			sout<<std::endl;

          //Parse bytes according to KISS protocol
          unsigned int jj = 0;
          if((pktbuf[0]!=KISS_FESC) && (pktbuf[0]!=KISS_FEND))
          {
            pktbufkiss[jj] = pktbuf[0];
            jj++;
          }
          for (unsigned int j=1;j<input_pkt_len; j++)
          {
            if (pktbuf[j-1]==KISS_FESC && pktbuf[j] == KISS_TFEND)
            {
              pktbufkiss[jj] = KISS_FEND;
              jj++;
            }
            else if(pktbuf[j-1]==KISS_FESC && pktbuf[j] == KISS_TFESC)
            {
              pktbufkiss[jj] = KISS_FESC;
              jj++;
            }
            else if((pktbuf[j] != KISS_FESC) && (pktbuf[j]!=KISS_FEND))
            {
              pktbufkiss[jj] = pktbuf[j];
              jj++;
            }
          }

          input_pkt_lenkiss = jj;

          // sout << "--------------------" << std::endl;
          // for(uint64_t p=0;p<input_pkt_lenkiss;p++)
          //   sout << " " << std::hex << (int)pktbufkiss[p];

          // sout << std::endl << "-----------------" << std::endl;
          //Create the complete packet from the data
          make_packet(pktarray, pktbufkiss);

          //Read out and scramble the data output
          n_onebits = 0;
          for (int j = 0; j<pkt_len; j++)
          {
            sout<<" "<<std::hex<<(int)pktarray[j];

            for(int k = 0; k < 8; k++)
            {
              bitout = (pktarray[j] & (1 << k))? 1 : 0;
              if (j < d_start_tx_delay && pktarray[j]==0xAA)
                //*out++ = bitout;
                *out++ = scramble(nrzi(bitout));
              else
                *out++ = scramble(nrzi(bitout));

              noutput_cnt++;

              if(bitout)
                n_onebits = n_onebits + 1;
              else
                n_onebits = 0;

              if(n_onebits==5 && j>= d_start_tx_delay && (j< (pkt_len - d_end_tx_delay)))
              {
                *out++ = scramble(nrzi(0));
                noutput_cnt++;
                n_onebits = 0;
              }

            }

          }
          sout<<std::endl;

          // remove_item_tag(i, tagoffset, d_tags_itr->key, d_tags_itr->value, pmt::mp(alias()));
          remove_item_tag(i, *d_tags_itr);
          add_item_tag(0, nitems_written(0), pmt::mp("ax25_len"), pmt::from_long((long) noutput_cnt*d_bit_oversampling*d_interp/d_decim), pmt::mp(alias()));
          // add_item_tag(0, nitems_written(0), pmt::mp("tag_two"), pmt::from_long((long) noutput_cnt*d_bit_oversampling*d_interp/d_decim), pmt::mp(alias()));
          //add_item_tag(0, nitems_written(0), pmt::mp("tx_sob"), pmt::PMT_T, pmt::mp(alias()));
          consume(i,input_pkt_len);         //Tell GNURADIO that one packet is being consumed

      }

      if(d_display) {
        sout << "----------------------------------------------------------------------";
        sout << std::endl;

        if(d_tags.size() > 0)
          std::cout << sout.str();
      }

      noutput_items = noutput_cnt;

      return noutput_items;
}
