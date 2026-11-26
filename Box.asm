
// Nand2Tetris Capstone - Box Program
// Roll Number: 2501730407
// K = 7
// Starting row = 7
// Width = 64 pixels (4 words)
// Height = 20 rows

(START)
    // Check whether any key is pressed
    @KBD
    D=M
    @DRAW
    D;JNE

    // If no key is pressed, erase the box
    @CLEAR
    0;JMP


// DRAW THE BOX
(DRAW)
    @16608
    D=A
    @row
    M=D

    @20
    D=A
    @rows
    M=D

(DRAW_ROW)
    @row
    D=M
    @addr
    M=D

    @4
    D=A
    @words
    M=D

(DRAW_WORD)
    @addr
    A=M
    M=-1

    @addr
    M=M+1

    @words
    MD=M-1
    @DRAW_WORD
    D;JGT

    @32
    D=A
    @row
    M=D+M

    @rows
    MD=M-1
    @DRAW_ROW
    D;JGT

    // Check keyboard again
    @START
    0;JMP


// ERASE THE BOX
(CLEAR)
    @16608
    D=A
    @row
    M=D

    @20
    D=A
    @rows
    M=D

(CLEAR_ROW)
    @row
    D=M
    @addr
    M=D

    @4
    D=A
    @words
    M=D

(CLEAR_WORD)
    @addr
    A=M
    M=0

    @addr
    M=M+1

    @words
    MD=M-1
    @CLEAR_WORD
    D;JGT

    @32
    D=A
    @row
    M=D+M

    @rows
    MD=M-1
    @CLEAR_ROW
    D;JGT

    // Return to keyboard checking
    @START
    0;JMP
