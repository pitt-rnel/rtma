// This is the SWIG interface file for the fundamental RTMA data types. The
// primary function is to generate wrappers for the message data structures, so
// that they may be imported into Python.
// Andrew S. Whitford 06/09
// JW Note 5/17/2019: This module does not seem necessary unless it becomes the primary method to translate message defs to Python. RTMA_types is included in PyRTMA (and potentially also in custom message defs)

%module RTMA_Definitions3
%{
#include "../../include/RTMA_types.h"
//#include "../../../src/Common/include/rp3_hst_config.h" // uncomment to include custom mdfs here (instead of separate module)
%}

%include "../../include/RTMA_types.h"
//%include "../../../src/Common/include/rp3_hst_config.h" // uncomment to include custom mdfs here (instead of separate module)

// Helper classes required for variable-length data.
%include "carrays.i"
%array_class(double, DoubleArray)
%array_class(unsigned char, UcharArray)

//swig -includeall -c++ -python rtma3.i
