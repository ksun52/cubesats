/*C++ block for EVM estimation*/

#ifdef HAVE_CONFIG_H
#include <config.h>
#endif

#include <mxlgs/mxlgs_evmest_cf.h>
#include <gnuradio/io_signature.h>
#include <math.h>
#include <iostream>
using namespace std;

mxlgs_evmest_cf_sptr mxlgs_make_evmest_cf (unsigned int npoints, unsigned int lvec, gr::digital::constellation_sptr cnst)
{
	return mxlgs_evmest_cf_sptr(new mxlgs_evmest_cf(npoints, lvec, cnst));
}

/*--------------------------------------------
 *		CONSTRUCTOR
 *-------------------------------------------*/
mxlgs_evmest_cf::mxlgs_evmest_cf(unsigned int npoints, unsigned int lvec, gr::digital::constellation_sptr cnst):sync_block("evm_estimator", gr::io_signature::make(1,1,sizeof(gr_complex)), gr::io_signature::make(1,1,sizeof(float))),d_cnst(cnst)
{
	d_npoints = npoints;
	d_Ps = 0;
	d_Pe = 0;
	d_evm = 0;
	d_lvec = lvec;
	constellation = d_cnst->points();
	num_points = d_cnst->arity();
	cout<<"number of points in the constellation is"<<num_points<<endl;
	constellation_scaled.resize(num_points*lvec);
	set_history(d_npoints-1);
}

/*--------------------------------------------
 *		DESTRUCTOR
 *------------------------------------------*/
mxlgs_evmest_cf::~mxlgs_evmest_cf()
{
}

/*-------------------------------------------
 *	      WORK FUNCTION
 *-----------------------------------------*/
int mxlgs_evmest_cf::work(int noutput_items,
			  gr_vector_const_void_star &input_items,
			  gr_vector_void_star &output_items)
{
	const gr_complex *in = (const gr_complex*) input_items[0];
	float *out = (float*)output_items[0];
	double nmean_squared, nmean;
	double enmean_squared;
	double mean_amp;
	error.resize(noutput_items);

	for(unsigned int n=d_npoints-1;n<noutput_items;n++){
		if(n<=d_npoints-1){
			nmean_squared = 0;
			nmean = 0;
			for(unsigned int j=0;j<=n;j++){
				nmean_squared = nmean_squared + pow(abs(in[n-j]),2);
				nmean = nmean + abs(in[n-j]);
			}
		}

		if(n > d_npoints-1){
			nmean_squared = nmean_squared+pow(abs(in[n]),2)-pow(abs(in[n-d_npoints]),2);
			nmean = nmean + abs(in[n]) - abs(in[n-d_npoints]);
		}

		d_Ps = (nmean_squared/d_npoints);
		mean_amp = nmean/d_npoints;
		
		//scale the constellation
		for(unsigned int i=0;i<num_points;i++){
			constellation_scaled[i] = constellation[i]*gr_complex(mean_amp,0);
		//	cout<<"constellation point "<<i<<" = "<<constellation_scaled[i]<<endl;
		}

		//find the minimum error vectors and compute its mean squared sum
		if(n<=d_npoints-1){
			enmean_squared=0;
			for(unsigned int j=0;j<=n;j++){
				emin=in[n-j]-constellation_scaled[0];
				for(unsigned int i=1;i<num_points;i++){
					if(abs(emin)>abs(in[n-j]-constellation_scaled[i]))
						emin = in[n-j]-constellation_scaled[i];
				}
				error[n-j]=emin;
				enmean_squared = enmean_squared + pow(abs(error[n-j]),2);
			}
		}

		if(n > d_npoints-1){
			emin=in[n]-constellation_scaled[0];
			for(unsigned int i=1;i<num_points;i++){
				if(abs(emin)>abs(in[n]-constellation_scaled[i]))
					emin = in[n]-constellation_scaled[i];
			}
			error[n]=emin;
		//	cout<<"input val = "<<in[n]<<"error = "<<emin<<endl;
			enmean_squared=enmean_squared + pow(abs(error[n]),2) - pow(abs(error[n-d_npoints]),2);
		}

		//use mean squared sum to compute error power
		d_Pe=(enmean_squared/d_npoints);

		out[n]=10*log10(d_Pe/d_Ps);
	}
//cout<<"mean_amp="<<mean_amp<<endl;
//cout<<"Ps="<<d_Ps<<endl;
//cout<<"Pe="<<d_Pe<<endl;


return noutput_items-d_npoints;
}

