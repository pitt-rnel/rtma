#include "Timing.h"
#include "OS_defines.h"

#ifdef _WINDOWS_C
// WINDOWS only h files
#include <windows.h>
#else
/*	LINUX   only h files*/
#include <sys/time.h>
#include <time.h>
#include <unistd.h>
#endif

/*Non OS specific h files*/

#ifdef _WINDOWS_C
// Global counter frequency value- used by GetAbsTime() on Windows
double win_counter_freq;
#endif

void InitializeAbsTime(void) {
#ifdef _WINDOWS_C
  LONGLONG freq = 0;
  QueryPerformanceFrequency((LARGE_INTEGER *)&freq);
  win_counter_freq = (double)freq;
#endif
}

double GetAbsTime(void)
// WIN: returns a seconds timestamp from a system counter
{
#ifdef _UNIX_C
  // The clocks Python's time.perf_counter() reads, so that modules in C++,
  // MATLAB and Python stamp messages on the same clock.
  struct timespec ts;
#ifdef __APPLE__
  const clockid_t clock = CLOCK_UPTIME_RAW; // mach_absolute_time()
#else
  const clockid_t clock = CLOCK_MONOTONIC;
#endif
  if (clock_gettime(clock, &ts) == 0)
    return ts.tv_sec + (ts.tv_nsec / 1e9);
  return 0.0;
#else
  LONGLONG current_time = 0;
  QueryPerformanceCounter((LARGE_INTEGER *)&current_time);
  return (double)current_time / win_counter_freq;
#endif
}
