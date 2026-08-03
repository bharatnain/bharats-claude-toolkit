#include <stdio.h> /* angle-bracket system include: must NOT appear as an edge */
#include "foo.h"   /* quoted include: edge main.c -> foo.h */

int main(void) {
    printf("%d\n", foo() + bar());
    return 0;
}
