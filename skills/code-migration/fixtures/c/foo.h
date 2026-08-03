#ifndef FOO_H
#define FOO_H
#include "bar.h" /* quoted include: edge foo.h -> bar.h (half of the header cycle) */
int foo(void);
#endif
