Instructions for Linux (see the wiki for further information):

Basic setup is performed by running make in the Python directory. If you have added new MDF structures, these need to create ctypes versions of the structure. Currently all MDFs in RTMA_types.h are present in RTMA_types.py, thanks to automatic code generators h2xml.py and xml2py.py. Possible options are:

    * adding RTMA_types.py manually, following the structure shown therein
    * add your MDF to a C header file RTMA_types.h and (re-)generating an associated Python version, like RTMA_types.py
    * add the type to your Python module directly 

The script example.py may be used to test the installation as follows:

   1. Start RTMA (i.e., CommandModule).
   2. Start the example producer (i.e., python example.py producer).
   3. Start the example consumer (i.e., python example.py consumer).
   4. Verify that the consumer receives messages sent by the producer. 

