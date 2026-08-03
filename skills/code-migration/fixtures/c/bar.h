#ifndef BAR_H
#define BAR_H
#include "foo.h" /* quoted include: edge bar.h -> foo.h (closes the header cycle) */
int bar(void);
#endif
