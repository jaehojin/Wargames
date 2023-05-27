from gdb, change the value of `$rbp-0x4` for each `cmp` instruction:

    (gdb) set *(int *)($rbp-0x4)=3/0/5

