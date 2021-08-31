// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

(INIT) 
	@8192
	D=A  // D = 8192
	@i                  
	M=D  // i = 8192

(LOOP)
	@i
	M=M-1  // i = i - 1
	D=M  // D = i
	@INIT 
	D;JLT  // if D < 0 goto INIT              
	@KBD
	D=M  // D = current key press ASCII
	@WHITE		        
	D;JEQ  // if D == 0 goto WHITE
	@BLACK
	0;JMP  // else goto BLACK

(BLACK)             
	@SCREEN            
	D=A  // D == address of 1st pixel
	@i
	A=D+M  // A = D + i
	M=-1  // Memory[A] = -1 (black pixels)
	@LOOP              
	0;JMP  // goto LOOP

(WHITE)
	@SCREEN            
	D=A                
	@i        
	A=D+M              
	M=0  // Memory[A] = 0 (whiten pixels)  
	@LOOP           
	0;JMP
