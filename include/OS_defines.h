#ifndef _OS_DEFINES_H_
#define _OS_DEFINES_H_

/* ----------------------------------------------------------------------------
   |                   OS to compile the code on                              |
   ----------------------------------------------------------------------------*/
#ifndef _OS_DEFINED
#define _OS_DEFINED TRUE
#if defined(_WIN32)
#ifndef _WINDOWS_C
#define _WINDOWS_C
#endif
#elif defined(__linux__)
#ifndef _UNIX_C
#define _UNIX_C
#endif
#ifndef _LINUX_C
#define _LINUX_C
#endif
#elif defined(__APPLE__)
#ifndef _UNIX_C
#define _UNIX_C
#endif
#ifndef _MAC_C
#define _MAC_C
#endif
#else
#error "RTMA supports Windows, Linux, and macOS only"
#endif
#endif

/* ----------------------------------------------------------------------------
   |                              DEFINES                                     |
   ----------------------------------------------------------------------------*/
#ifdef _UNIX_C
#define TRUE 1
#define FALSE 0
#else
#define _CRT_SECURE_NO_DEPRECATE 1 // prevent vs2005 deprecated warning
#define _CRT_SECURE_NO_WARNINGS 1  // disable deprecations
#endif

#ifdef _UNIX_C
#define THIS_MODULE_BASE_PRIORITY 0
#define NORMAL_PRIORITY_CLASS 1
#else
#define THIS_MODULE_BASE_PRIORITY 0x00008000 // ABOVE_NORMAL_PRIORITY_CLASS
// #define THIS_MODULE_BASE_PRIORITY
// ABOVE_NORMAL_PRIORITY_CLASS//ABOVE_NORMAL_PRIORITY_CLASS
// NORMAL_PRIORITY_CLASS
#endif

/*
#ifdef _UNIX_C
        #include <sys/types.h> //for getpid()
        #include <unistd.h>    //for getpid()
        #include <sys/time.h>  //for gettimeofday()
        #include <signal.h>
#else
        #include <windows.h>
#endif
*/

#endif //_OS_DEFINES_H_
