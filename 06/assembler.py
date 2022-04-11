import sys


if len(sys.argv) != 3:
    raise AttributeError("assembler needs 2 args!")

inpf, outf = sys.argv[1:]

if inpf.split(".")[1] != "asm":
    raise AttributeError("input not .asm file!")

open(outf, "w").close()

outf = open(outf, "a")
inpf = open(inpf, "r")

RAM = 16

JUMP = {"null": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
        "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}

COMP = {"0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", 
        "M": "1110000", "!D": "0001101", "!A": "0110001", "!M": "1110001", "-D": "0001111", 
        "-A": "0110011", "-M": "1110011", "D+1": "0011111", "A+1": "0110111", "M+1": "1110111", 
        "D-1": "0001110", "A-1": "0110010", "M-1": "1110010", "D+A": "0000010", "A+D": "0000010", 
        "D+M": "1000010", "M+D": "1000010", "D-A": "0010011", "D-M": "1010011", "A-D": "0000111", 
        "M-D": "1000111", "D&A": "0000000", "A&D": "0000000", "D&M": "1000000", "M&D": "1000000", 
        "D|A": "0010101", "A|D": "0010101", "D|M": "1010101", "M|D": "1010101"}

DEST = {"null": "000", "M": "001", "D": "010", "MD": "011",
        "A": "100", "AM": "101", "AD": "110", "AMD": "111"}

SYM = {"SCREEN": "0100000000000000", "KBD": "0110000000000000", "SP": "0000000000000000",
       "LCL": "0000000000000001", "ARG": "0000000000000010", "THIS": "0000000000000011",
       "THAT": "0000000000000100", "R0": "0000000000000000", "R1": "0000000000000001",
       "R2": "0000000000000010", "R3": "0000000000000011", "R4": "0000000000000100",
       "R5": "0000000000000101", "R6": "0000000000000110", "R7": "0000000000000111",
       "R8": "0000000000001000", "R9": "0000000000001001", "R10": "0000000000001010",
       "R11": "0000000000001011", "R12": "0000000000001100", "R13": "0000000000001101",
       "R14": "0000000000001110", "R15": "0000000000001111"}


def assemble(I):
    global RAM
    for i in I:
        dcj = i.split(";")
        dc = dcj[0]
        j = dcj[-1] if len(dcj) == 2 else "null"
        eq = dc.split("=")
        c = eq[-1]
        d = eq[0] if len(eq) == 2 else "null"
        if i[0] == "@":
            v = i[1:]
            if v.isnumeric():
                A = bin(int(v))[2:]
                outf.write("0" * (16 - len(A)) + A + "\n")
            elif v in SYM:
                outf.write(SYM[v] + "\n")
            else:
                A = bin(int(RAM))[2:]
                t = "0" * (16 - len(A)) + A
                SYM[v] = t
                RAM += 1
                outf.write(t + "\n")
        else:
            outf.write("111" + COMP[c] + DEST[d] + JUMP[j] + "\n")


def clean(I):
    f = []
    for i in I:
        if i:
            if i[0] != "/":
                i = i.split("//")[0]
                for j in range(len(i) - 1, -1, -1):
                    if i[j] != " ":
                        break
                i = i[:j + 1]
                for j in range(len(i)):
                    if i[j] != " ":
                        break
                i = i[j:]
                if i[0] == "(":
                    v = i[1:-1]
                    if v not in SYM:
                        a = bin(int(len(f)))[2:]
                        SYM[v] = "0" * (16 - len(a)) + a
                    continue
                f.append(i)
    return f


assemble(clean(inpf.read().split("\n")))
