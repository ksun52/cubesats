#!/usr/bin/sh
export VOLK_GENERIC=1
export GR_DONT_LOAD_PREFS=1
export srcdir=/home/pi/plutoradio/PlutoRadio/gr-mxlgs/lib
export PATH=/home/pi/plutoradio/PlutoRadio/gr-mxlgs/build/lib:$PATH
export LD_LIBRARY_PATH=/home/pi/plutoradio/PlutoRadio/gr-mxlgs/build/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$PYTHONPATH
test-mxlgs 
