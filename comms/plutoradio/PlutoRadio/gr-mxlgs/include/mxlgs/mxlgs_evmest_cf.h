/*This block measures the Average Error Vector Magnitude (EVM) over 10000 samples.
 *MXLab, University of Michigan, Ann Arbor
 *Srinagesh Sharma
 */

#ifndef INCLUDED_MXLGS_EVMEST_CF_H
#define INCLUDED_MXLGS_EVMEST_CF_H

//#include <gnuradio/core_api.h>
#include <mxlgs/api.h>
#include <gnuradio/sync_block.h>
#include <gnuradio/digital/constellation.h>
#include <math.h>

class mxlgs_evmest_cf;
typedef boost::shared_ptr<mxlgs_evmest_cf> mxlgs_evmest_cf_sptr;
MXLGS_API mxlgs_evmest_cf_sptr mxlgs_make_evmest_cf(unsigned int npoints, unsigned int lvec, gr::digital::constellation_sptr cnst);

class MXLGS_API mxlgs_evmest_cf: public gr::sync_block
{
private:
friend MXLGS_API mxlgs_evmest_cf_sptr mxlgs_make_evmest_cf(unsigned int npoints, unsigned int lvec, gr::digital::constellation_sptr cnst);
mxlgs_evmest_cf(unsigned int npoints, unsigned int lvec, gr::digital::constellation_sptr cnst);

gr::digital::constellation_sptr d_cnst;
double d_Ps;
double d_Pe;
double d_evm;
unsigned int d_npoints;
unsigned int d_lvec;
unsigned int num_points;
gr_complex emin;
std::vector<gr_complex> constellation;
std::vector<gr_complex> constellation_scaled;
std::vector<gr_complex> error;

public:
~mxlgs_evmest_cf();

int work (int noutput_items,
	  gr_vector_const_void_star &input_items,
	  gr_vector_void_star &output_items);
};

#endif
