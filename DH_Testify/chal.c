#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <fcntl.h>
#include <malloc.h>
#include <stdbool.h>

#define FLAG_HEADER "DH{"
#define FLAG "real flag is [0-9a-f]{64}. Have a nice day!\0"
#define FLAG_FOOTER "}"
#define nullptr NULL

struct node *head;

struct node
{
    int wire_amount;
    char *str;
    struct node *fail;
    struct wire *wire[0x100];
};

struct wire
{
    char ch;
    struct node *next;
};

void err(const char *err_str)
{
    puts(err_str);
    exit(-1);
}

struct node *go(struct node *curr, char ch)
{
    for(int i=0; i<curr->wire_amount; i++)
        if(curr->wire[i]->ch == ch)
            return curr->wire[i]->next;
    return nullptr;
}

void gen_fail(struct node *curr)
{
    struct node *next = nullptr;

    for(int i=0; i < curr->wire_amount; i++)
    {
        next = nullptr;
        if((next = go(curr->fail, curr->wire[i]->ch)) == nullptr || next == curr->wire[i]->next)
            curr->wire[i]->next->fail = head;
        else
            curr->wire[i]->next->fail = next;
    }

    for(int i=0; i < curr->wire_amount; i++)
        gen_fail(curr->wire[i]->next);
}

struct node *fail(struct node *curr)
{
    return curr->fail;
}

void testify()
{
    struct node *curr = head;
    struct node *next = nullptr;
    char *curr_str = FLAG;

    while(*curr_str != '\0')
    {
        if((next = go(curr, *curr_str)) == nullptr)
        {
            if(curr != head)
                curr = fail(curr);
            else
                *curr_str++;
        }
        else 
        {
            curr = next;
            if(curr->str != nullptr)
            {
                printf("pure!\n");
                return;
            }
            curr_str++;
        }
    }
    printf("fail...\n");
}

int generate_testify()
{
    int amount;
    printf("amount: ");
    scanf("%d", &amount);

    if(amount < 0x0)
        err("Sorry, Your input value is too small");
    if(amount > 0x100)
        err("Sorry, Your input value is too large");

    char **arr = (char **)malloc(sizeof(char *) * amount);
    for(int i=0; i<amount; i++)
        arr[i] = (char *)malloc(sizeof(char) * 0x10);
    
    for(int i=0; i<amount; i++)
    {        
        int detect;
        printf("input %d: ", i+1);
        arr[i][(detect = read(0, arr[i], 0x10))] = '\x00';
        if(detect <= 0 || arr[i][0] == '\n')
            err("None Input or Read err");
        if(arr[i][detect-1] == '\n')
            arr[i][detect-1] = '\x00';  
    }

    head = (struct node *)malloc(sizeof(struct node));
    head->str = nullptr; head->wire_amount = 0; head->fail = head;

    for(int i=0; i<amount; i++)
    {
        struct node *curr = head;
        char *curr_str = arr[i];

        while(true)
        {   
            bool find = false;
            for(int j=0; j<curr->wire_amount; j++)
                if(curr->wire[j]->ch == *curr_str)
                {
                    curr = curr->wire[j]->next;
                    find = true;
                    break;
                }

            if(find == false)
            {
                curr->wire[curr->wire_amount] = (struct wire *)malloc(sizeof(struct wire));
                curr->wire[curr->wire_amount]->ch = *curr_str;

                curr->wire[curr->wire_amount]->next = (struct node *)malloc(sizeof(struct node));
                curr->wire[curr->wire_amount]->next->wire_amount = 0;
                curr->wire[curr->wire_amount]->next->str = nullptr;
                curr->wire[curr->wire_amount]->next->fail = nullptr;
                
                curr->wire_amount++;

                curr = curr->wire[curr->wire_amount-1]->next;
            }

            curr_str++;

            if(*curr_str == '\0')
            {
                if(curr->str == nullptr)
                {
                    int len = curr_str - arr[i];
                    curr->str = (char *)malloc(sizeof(char) * (len+1));
                    strncpy(curr->str, arr[i], len);
                    curr->str[len] = '\0';
                }
                
                break;
            }
        }
    }
    gen_fail(head);

    testify();
}

int main()
{
    setvbuf(stdin, 0, 2, 0);
    setvbuf(stdout, 0, 2, 0);
    setvbuf(stderr, 0, 2, 0);

    puts("---------- Testify ----------");

    while(true)
    {
        char ch[2] = "n";

        generate_testify();

        printf("Try Again? [Y/n]: ");
        scanf("%2s", ch);

        if(ch[0] == 'N' || ch[0] == 'n')
            return 0;
    }
}

