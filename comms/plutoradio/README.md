# PlutoRadio

This project includes software required to run radio programs to interact with the ADALM-Pluto SDR. See Pluto integration document for more information.

## gr-mxlgs

Contains gnuradio software for a FSK modulation scheme using the PlutoSDRs. Pluto's drivers are required for this software to run. All applications are stored in gr-mxlgs/apps/.

## CFLTXRX

Contains example software for sending and receiving bytes from the radio software mentioned above. This example software sends a RAP beacon every few seconds to the radio software for transmission.

**See Pluto integration document for more information.**
