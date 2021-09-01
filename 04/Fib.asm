// test program
// cycle through 1st 13 Fibonacci numbers again and again

(LOOP)
    @x
    M=0
    @y
    M=1
    @z
    M=0
    D=M
    (FIB)
        @255
        D=D-A
        @LOOP
        D;JGE
        @x
        D=M
        @y
        D=D+M
        @z
        M=D
        @y
        D=M
        @x
        M=D
        @z
        D=M
        @y
        M=D
        @FIB
        0;JMP
