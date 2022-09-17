#include <stdio.h>
#include <stdlib.h>

int main(void){
	char a[20]="AAAAAAAAAA";
	int *ip = (int*)a;
	printf("%s\n", a);
	printf("%d\n", *a);
	printf("%d\n", *ip);
	return 0;
}
