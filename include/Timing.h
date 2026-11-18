#ifndef _TIMING_H_
#define _TIMING_H_

void InitializeAbsTime(
    void); // Must be called in Windows before using GetAbsTime

double
GetAbsTime(void); // Gets a timestamp in seconds from a monotonic system
                  // clock, the one pyrtma's time.perf_counter() reads:
                  // QueryPerformanceCounter() on Windows, CLOCK_MONOTONIC on
                  // Linux and CLOCK_UPTIME_RAW (mach_absolute_time()) on
                  // macOS. Its zero is arbitrary, usually when the machine
                  // booted, so it is for times relative to each other, on one
                  // machine, and not for dates. Message headers' send_time and
                  // recv_time are in it, so C++, MATLAB and Python modules
                  // stamp messages on the same clock. This is a low-overhead
                  // function, accurate to at least the nearest microsecond.

#endif //_TIMING_H_
