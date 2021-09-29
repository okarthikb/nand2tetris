# Assembler

This is project 06 of nand2tetris, in which we make a simple assembler to conver the Hack assembly language into 16-bit machine code for the Hack architecture. To assemble a .asm file, run the command

```$ python3 path\to\assembler.py 'path\to\input\file.asm' 'path\to\store\output\file.hack'```

To check if it has been correctly assembled, run the command

```$ python3 path\to\compare.py 'path\to\your\output\file.hack' 'path\to\other\output\file.hack'```

Prints "True" if correct, else "False" and line where error occured.
