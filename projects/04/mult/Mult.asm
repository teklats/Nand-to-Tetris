// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/4/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)
// The algorithm is based on repetitive addition.

//// Replace this comment with your code.

// Pseudocode

// i = 0;
// mul = 0;

// LOOP: 
//	if (i > R0) goto STOP
//	mul = mul + R1
//	i = i + 1
// STOP:
//	R2 = mul;

@i
M = 1  // i = 1

@mul
M = 0  // mul = 0

(LOOP)
	@i
	D = M
	@R0
	D = D - M  // D = i - a
	@STOP
	D; JGT	// if i - R0 > 0 goto STOP

	@mul
	D = M  
	@R1
	D = D + M  // D = D + R1

	@mul
	M = D  // mul = D

	@i
	M = M + 1  // i = i + 1

	@LOOP
	0; JMP


(STOP)
	@mul
	D = M  // D = mul

	@R2
	M = D  // R2 = mul

(END)
	@END
	0; JMP



