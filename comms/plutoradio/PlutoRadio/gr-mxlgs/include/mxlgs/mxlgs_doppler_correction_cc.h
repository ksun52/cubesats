/* This block implements a doppler correction for gnu radio. It reads frequency from a local port and interfaces with gpredict. It also sets a source with a complex sinewave with this frequency and mixes it with the input. effectively working as a doppler shift system */

#ifndef INCLUDED_MXLGS_DOPPLER_CORRECTION_CC_H
#define INCLUDED_MXLGS_DOPPLER_CORRECTION_CC_H

//#include <gr_core_api.h>
#include <mxlgs/api.h>
#include <gnuradio/sync_block.h>
#include <gnuradio/fxpt_nco.h>
#include <fstream>
#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

class mxlgs_doppler_correction_cc;
typedef boost::shared_ptr<mxlgs_doppler_correction_cc> mxlgs_doppler_correction_cc_sptr;
MXLGS_API mxlgs_doppler_correction_cc_sptr mxlgs_make_doppler_correction_cc (double sampling_freq, unsigned int port, int dir, double int_freq, long int rxfreq);

class MXLGS_API mxlgs_doppler_correction_cc: public gr::sync_block
{
private:
friend MXLGS_API mxlgs_doppler_correction_cc_sptr mxlgs_make_doppler_correction_cc (double sampling_freq, unsigned int port, int dir, double int_freq, long int rxfreq);
mxlgs_doppler_correction_cc(double sampling_freq, unsigned int port, int dir, double int_freq, long int rxfreq);

double d_sampling_freq;
double d_int_freq;
unsigned int d_port;
int d_dir;
double d_local_freq;
double d_doppler;
long int d_rxfreq;
gr::fxpt_nco d_nco;
pthread_t socket_thread;

static void *start_thread(void *obj){
	reinterpret_cast<mxlgs_doppler_correction_cc *>(obj)->socket_thread_work();
}

public:
~mxlgs_doppler_correction_cc();

void socket_thread_work();

int process_command(char*, char*);

int work (int noutput_items,
	  gr_vector_const_void_star &input_items,
          gr_vector_void_star &output_items);
};

#endif
