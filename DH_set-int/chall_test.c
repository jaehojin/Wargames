// Name: chall.c
// Compile: gcc chall.c -o chall -no-pie -fno-stack-protector

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>

void alarm_handler()
{
    puts("TIME OUT");
    exit(-1);
}

void initialize()
{
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);

    signal(SIGALRM, alarm_handler);
    alarm(30);
}

int main(int argc, char *argv[])
{
    unsigned int a = 0;
    int b = 0;

    initialize();

    printf("Your input : \n");
    a = 4294967295;
    if (a > 0)
    {
        b = (int)a + 1;
        if (b == 0)
        {
            printf("Success.\nYour second input : \n");
            scanf("%d", &b);
            if (b < 1)
            {
                b = b - 1;
                if (b > 0)
                {
                    system("/bin/sh");
                }
                else
                {
                    printf("fail!\n");
                }
            }
            else
            {
                printf("Input is too large!\n");
            }
        }
        else
        {
            printf("fail!\n");
        }
    }
    else
    {
        printf("Input is too small!\n");
    }

    return 0;
}