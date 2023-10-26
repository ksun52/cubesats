/* -*- c++ -*- */
/* Michigan eXploration Laboratory
 * This GNURADIO block performs AX-25 packetization on 
 * a tagged stream.
 * Author: Srinagesh Sharma 
 */


#ifndef INCLUDED_MXLGS_AX25_PACKETIZATION_H
#define INCLUDED_MXLGS_AX25_PACKETIZATION_H

#undef VERBOSE

#include <mxlgs/api.h>
#include <gnuradio/block.h>
#include <gnuradio/thread/thread.h>
#include <stddef.h>
#include <gnuradio/blocks/pdu.h>

#define MAX_PACKET_LEN 16384
#define MIN_PACKET_LEN 17
#define FLAG 0x7E

class mxlgs_ax25_packetization;
typedef boost::shared_ptr<mxlgs_ax25_packetization> mxlgs_ax25_packetization_sptr;

MXLGS_API mxlgs_ax25_packetization_sptr mxlgs_make_ax25_packetization(unsigned int start_tx_delay, unsigned int end_tx_delay, float bit_oversampling, float interp, float decim);

class MXLGS_API mxlgs_ax25_packetization : public gr::block
{
private:
	friend MXLGS_API mxlgs_ax25_packetization_sptr mxlgs_make_ax25_packetization(unsigned int start_tx_delay, unsigned int end_tx_delay, float bit_oversampling, float interp, float decim);
	//typedef boost::shared_ptr<mxlgs_ax25_packetization> mxlgs_ax25_packetization_sptr;

	//static mxlgs_ax25_packetization_sptr mxlgs_make_ax25_packetization(unsigned int start_tx_delay, unsigned int end_tx_delay);

	mxlgs_ax25_packetization(unsigned int start_tx_delay, unsigned int end_tx_delay, float bit_oversampling, float interp, float decim);
		
	//std::string d_name;
	unsigned int d_start_tx_delay, d_end_tx_delay;
	std::vector<gr::tag_t> d_tags;
	std::vector<gr::tag_t>::iterator d_tags_itr;
	bool d_display;
	gr::thread::mutex d_mutex;
	uint8_t *pktbuf, *pktbufkiss, *pktarray;
	unsigned int pkt_len;
	unsigned int input_pkt_len, input_pkt_lenkiss;

	unsigned char *dest_id, *source_id;
	unsigned int dest_length, source_length;
	unsigned char control, pid;
	unsigned char fcshi, fcslo;

	unsigned int noutput_cnt;
	unsigned int n_onebits;
	unsigned char bitout;
	float d_bit_oversampling;
	float d_interp;
	float d_decim;

public:
	~mxlgs_ax25_packetization();

	std::vector<gr::tag_t> current_tags();

	void set_display(bool d);
	void make_packet(unsigned char *pktarray, unsigned char *pktbufkiss);

	int general_work(int noutput_items,
		gr_vector_int &ninput_items,
		gr_vector_const_void_star &input_items,
		gr_vector_void_star &output_items);
};

#endif
