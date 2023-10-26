/* -*- c++ -*- */
/*
 * Michigan eXploration Labs
 * Stream to PDU with AX-25 packetization protocol
 * Author: Srinagesh Sharma
 */

#ifdef HAVE_CONFIG_H
#include "config.h"
#endif

#include <mxlgs/mxlgs_stream_to_pdu.h>
#include <gnuradio/blocks/pdu.h>
#include <gnuradio/io_signature.h>
#include <assert.h>
#include <stdexcept>
#include <stdio.h>
#include <iostream>
#undef VERBOSE
#define VERBOSE

#define KISS_FEND 0xC0
#define KISS_FESC 0xDB
#define KISS_TFEND 0xDC
#define KISS_TFESC 0xDD

mxlgs_stream_to_pdu_sptr mxlgs_make_stream_to_pdu (bool mode)
{
	return mxlgs_stream_to_pdu_sptr (new mxlgs_stream_to_pdu(mode));
}

mxlgs_stream_to_pdu::mxlgs_stream_to_pdu (bool mode)
	: sync_block ("stream_to_pdu",
			gr::io_signature::make (1, 1, sizeof (unsigned char)),
			gr::io_signature::make (0,0,0)),
	mode(mode),
	d_itemsize(sizeof(unsigned char)),
	d_inpdu(false),
	d_type(gr::blocks::pdu::byte_t),
	d_pdu_meta(pmt::PMT_NIL),
	d_pdu_vector(pmt::PMT_NIL)
		{
			message_port_register_out(pmt::mp("pdus"));
			state = STARTFLAG;
			pktbuf = new uint8_t [MAX_PACKET_LEN];
			pktkiss = new uint8_t [MAX_PACKET_LEN];
			sr=0;
			prevbit=0;
			descr=0;
			d_signalstatus=0;
			std::cout<<"passed the PDU constructor"<<std::endl;
		}

static unsigned short checkfcs(unsigned char *pktbuf, int bytecount) {
	unsigned short fcs=0xFFFF;
	for (int i=0; i<bytecount-2; i++) {
		fcs = fcs ^ *pktbuf++;
		for (int k=0;k<8;k++) {
			if (fcs & 0x01) fcs = (fcs >> 1) ^ 0x8408;
			else fcs>>=1;
		}
	}
	return(fcs^0xFFFF);
}

static char* int2bin(int a) {
	static char str[64];
	int cnt=15;
	while (cnt > -1) {
		str[cnt--]=(a & 0x01)?'1':'0';
		a>>=1;
	} 
	return str;
} 

static char* char2bin(char a) {
	static char str[64];
	int cnt=7;
	while (cnt > -1) {
		str[cnt--]=(a & 0x01)?'1':'0';
		a>>=1;
	} 
	return str;
}

void mxlgs_stream_to_pdu::send_message()
{
	if (pmt::length(d_pdu_vector) != d_pdu_length)
	throw std::runtime_error("msg length not correct");

	pmt::pmt_t msg = pmt::cons(d_pdu_meta, d_pdu_vector);
	message_port_pub(pmt::mp("pdus"), msg);

	d_pdu_meta = pmt::PMT_NIL;
	d_pdu_vector = pmt::PMT_NIL;
	d_pdu_length = 0;
	d_pdu_remain = 0;
	d_inpdu = false;
	return;
}

int mxlgs_stream_to_pdu::work (int noutput_items,
							gr_vector_const_void_star &input_items,
							gr_vector_void_star &output_items)
{
	const unsigned char *in = (const unsigned char *) input_items[0];
	//int *out = (int*) output_items[0];
	int ii=0;
	int n=0;
	while (n < noutput_items){
		bit=*in;

		//LFSR descrambling
		if (mode) {
			rbit=((descr>>11) & 1) ^ ((descr>>16) & 1) ^ bit;		
			descr<<=1;
			descr|=bit;
			bit=rbit;
		}

		//NRZI decoding
		if (prevbit==bit) rbit=1;									
		else rbit=0;
		prevbit=bit;

#ifdef VERBOSE
						//printf("Got %d (%d)\n",rbit,bit);
#endif 

		switch (state) {
			case STARTFLAG:			//looking for start of head flags
				sr>>=1;
				if (rbit==1) sr|=0x80;
				if (sr==FLAG) {
					state=PACKET;
					bitctr=0;
					flagctr=1;
#ifdef VERBOSE
					//				printf("Start of Head Flags Found\n");
					//head flags have been found so start recording SNR, output 1
#endif 				
					d_signalstatus=0;
				}
				break;
			case PACKET:			//looking for packet start (end of head flags)
				sr>>=1;
				if (rbit==1) sr|=0x80;
				bitctr++;
				if (bitctr==8) {
					bitctr=0;
					if (sr!=FLAG && flagctr > 2) {
						state=ENDFLAG;
						pktptr=pktbuf;
						*pktptr=sr;
						pktptr++;
						bytectr=1;
						ones=0;
						printf("....There were %d flags....\n",flagctr);
						//set output to 1: record SNR
						d_signalstatus=1;
#ifdef VERBOSE
						printf("Start of Packet Found %02X after %d FLAGS\n",sr,flagctr);
#endif					
					}
					else if (sr != FLAG) {
						state = STARTFLAG;
						if(flagctr > 4)
							printf("....There were only %d flags....",flagctr);
						/*
						printf("the next was 0x%02x.\n",sr);
						printf("FLAG = 0x%02X\n",FLAG);
						*/
					}
					else {
						flagctr++;
#ifdef VERBOSE
//						printf("Got FLAG\n");
#endif						
					}
				}
				break;
			case ENDFLAG:					//looking for start of tail flags
				//printf("\tGot %d (%d) %d\n",rbit,bit, ones);
				if (ones==5) {
					if (rbit==0) {	//destuffing
#ifdef VERBOSE					
						printf ("\n\nDESTUFFING!!! %d %d\n\n", ones,bytectr);
						fflush(stdout);
#endif
					}
					else {					//6 bits in a row - FLAG!
						state=LASTFLAGBIT;	//we need to consume one more bit (last 0 of the flag)
#ifdef VERBOSE
						printf("End of Packet Found (%d bytes)\n",bytectr);
						
#endif
						//set output to 0
						d_signalstatus=0;
						if (bytectr>=MIN_PACKET_LEN) {					//check CRC and if OK send to out queue
							unsigned short gfcs = pktbuf[bytectr-1];
							gfcs=(gfcs<<8)|pktbuf[bytectr-2];
							unsigned short cfcs = checkfcs(pktbuf,bytectr);
							printf("\tGFCS CFCS %X %X\n", gfcs, cfcs);


// jwc working here
							if (gfcs!=cfcs) {
								// Check sum failed.  Add a special Lithium check,
								// since we think the Lithium is bit stuffing poorly.
								// See #13962 for details.
								// Check if last byte was a 0x7E.  If so, then assume 
								// it's a flag and remove it from the buffer.
								if ( pktbuf[bytectr-1] == 0x7E && bytectr == 256 )
								{
									bytectr--;
									gfcs = pktbuf[bytectr-1];
									gfcs=(gfcs<<8)|pktbuf[bytectr-2];
									cfcs = checkfcs(pktbuf,bytectr);

									/*
									gfcs = pktbuf[bytectr-1-1];
									gfcs=(gfcs<<8)|pktbuf[bytectr-2-1];
									cfcs = checkfcs(pktbuf,bytectr-1);
									*/

									if (gfcs==cfcs) 
										printf("\tGFCS CFCS %X %X -- modified\n", gfcs, cfcs);
								}
							}

							//gfcs = pktbuf[bytectr-1];
							//gfcs=(gfcs<<8)|pktbuf[bytectr-2];
							//cfcs = checkfcs(pktbuf,bytectr);


							if (gfcs==cfcs) {
								printf("\nCRC2 %X %X\n",gfcs,cfcs);
								for(ii = 0; ii < bytectr; ii++)
								{
									if ( ii % 16 == 0 )
										printf("\n\t");
									printf("%02X ", pktbuf[ii]);
								}
								printf("\n");
								std::cout<<"\n\tLength:"<<bytectr<<std::endl; 
								bytectr-=2;

								//modify packet buff with KISS_FEND and KISS_FESC
								unsigned int jj=0;
								pktkiss[0] = KISS_FEND;
								pktkiss[1] = 1;
								jj = 2;
								for(ii=0; ii<bytectr;ii++){
									uint8_t curbyte = pktbuf[ii];
									if(curbyte==KISS_FEND){
										pktkiss[jj] = KISS_FESC;
										pktkiss[jj+1] = KISS_TFEND;
										jj=jj+2;
									}
									else if(curbyte == KISS_FESC){
										pktkiss[jj]=KISS_FESC;
										pktkiss[jj+1]=KISS_TFESC;
										jj=jj+2;
									}
									else{
										pktkiss[jj]=curbyte;
										jj++;
									}
								}
								pktkiss[jj] = KISS_FEND;
								bytekissctr = jj+1;

								d_pdu_length =bytekissctr;
								d_pdu_meta = pmt::make_dict();
								d_pdu_vector = pmt::init_u8vector(bytekissctr, pktkiss);
								//std::cout<<"length:"<<bytekissctr<<std::endl; 
								send_message();	    
								printf("\n\n");
							}
							else 
							{
								printf("\tX Checksum failed X\n");
								for(ii = 0; ii < bytectr; ii++){
									if ( ii % 16 == 0 )
										printf("\n\t");
									printf("%02X ", pktbuf[ii]);
								}
								std::cout<<"\n\tLength:"<<bytectr<<std::endl; 
								fflush(stdout);
							}
						}					
					}
				}
				else {
					*pktptr>>=1;
					if (rbit==1) *pktptr|=0x80;
					bitctr++;
					if (bitctr==8) {
						bitctr=0;
#ifdef VERBOSE
						printf("Got BYTE %02X %s (%d)\n",*pktptr,char2bin(*pktptr),bytectr);
#endif						
						pktptr++;
						bytectr++;
					}
				}	
				if (rbit==1) ones++;
				else ones=0;
				break;
			case LASTFLAGBIT:		//just consume a bit
				state=STARTFLAG;
				sr=0;
				bitctr=0;
				//make output 0: stop recording SNR
				d_signalstatus=0;
				break;
			case END:				//looking for end of tail flags
				sr>>=1;
				if (rbit==1) sr|=0x80;
				bitctr++;
				if (bitctr==8) {
					bitctr=0;
					if (sr!=FLAG) {
						state=STARTFLAG;
						sr=0;			
#ifdef VERBOSE
						printf("End of Tail Flags Found\n");
#endif					
						//set output to 0: stop recording SNR
						d_signalstatus=0;
					}
					else {
#ifdef VERBOSE
//						printf("Got FLAG\n");
#endif						
					}
				}
				break;
		}
		//*out++=d_signalstatus;
		in++;
		n++;
	}
	return n;
}
