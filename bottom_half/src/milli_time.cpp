#include "milli_time.h"
unsigned long getPeriod(unsigned long new_time, unsigned long old)
{
    if (new_time > old) return new_time - old;
    else {
        // in case of overflow
        return new_time + (((unsigned long)-1) - old) + 1;
    }
}
