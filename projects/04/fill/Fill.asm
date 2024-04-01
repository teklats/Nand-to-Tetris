// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, 
// the screen should be cleared.

//// Replace this comment with your code.


// Pseudocode

// curr = SCREEN;
// end = 24575;

//	LOOP:
//		if (KBD > 0) goto BLACK
//		goto WHITE

//	BLACK:
//		if (end - curr < 0) goto LOOP
//		RAM[curr] = -1;
//		curr = curr + 1;
//		goto LOOP

//	WHITE:
//		if (SCREEN - curr < 0) goto LOOP
//		RAM[curr] = 0;
//		curr = curr - 1;
//		goto LOOP


@SCREEN
D = A
@curr
M = D // curr == SCREEN (curr address of screen)


@24575
D = A
@end
M = D // end == KBD - 1 == last bit of screen

(LOOP)
    @KBD
    D = M
    @BLACK
    D;JGT

    @WHITE
    0;JMP

(BLACK)
    @end
    D = M
    @curr
    D = D - M

    @LOOP
    D; JLT // if end - curr < 0 goto LOOP

    @curr
    D = M
    A = M
    M = -1 // RAM[curr] = -1; black pixel

    @curr
    M = D + 1 // curr = D + 1; go to next bit

    @LOOP
    0;JMP

(WHITE)
    @SCREEN
    D = A
    @curr
    D = D - M

    @LOOP
    D; JGT // if SCREEN - curr > 0 got LOOP

    @curr
    D = M
    A = M
    M = 0 // RAM[curr] = 0; white pixel

    @curr
    M = D - 1 // curr = D - 1; go to prev bit

    @LOOP
    0;JMP
