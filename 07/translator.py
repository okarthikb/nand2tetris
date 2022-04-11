# VM translator, input .vm file outputs .asm file


from re import sub
from sys import argv


seg = {"local": "LCL", "argument": "ARG", "this": "3", "that": "4"}
adr = {"static": 16, "pointer": 3, "temp": 5}
bo = {"add": "+", "sub": "-", "and": "&", "or": "|"}
cmp = {"eq": "JEQ", "gt": "JGT", "lt": "JLT"}
uo = {"neg": "-", "not": "!"}

cmpn = {"eq": -1, "gt": -1, "lt": -1}

uos = """@SP
A=M-1
M=oM"""  # unary op

bos = """@SP
M=M-1
A=M
D=M
A=A-1
M=MoD"""  # binary op

cmps = """@SP
M=M-1
A=M
D=M
A=A-1
D=M-D
@ifo_
D;o
D=0
@eifo_
0;JMP
(ifo_)
D=-1
(eifo_)
@SP 
A=M-1
M=D"""  # compare

push0 = """@seg
D=M
@_
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1"""  # push seg _

push1 = """@_
D=M
@SP
A=M
M=D
@SP
M=M+1"""  # push adr _

push2 = """@_
D=A
@SP
A=M
M=D
@SP
M=M+1"""  # push constant _

pop0 = """@_
D=A
@seg
M=M+D
@SP
M=M-1
A=M
D=M
@seg
A=M
M=D
@_
D=A
@seg
M=M-D"""  # pop seg _

pop1 = """@SP
M=M-1
A=M
D=M
@_
M=D"""  # pop adr _

dct = {"push": (push0, push1, push2), "pop": (pop0, pop1)}


def parse(s):
  s = s.split(" ")
  if len(s) == 1:
    if s[0] in cmp:
      cmpn[s[0]] += 1
      return sub("_", f"{cmpn[s[0]]}", sub("o", cmp[s[0]], cmps))
    else:
      op, ops = (uo[s[0]], uos) if s[0] in uo else (bo[s[0]], bos)
      return sub("o", op, ops)
  else:
    i = 2 if s[1] == "constant" else 1 if s[1] in adr else 0
    s[2] = f"{adr[s[1]] + int(s[2])}" if s[1] in adr else s[2]
    res = sub("_", s[2], dct[s[0]][i])
    return res if i != 0 else sub("seg", seg[s[1]], res)


def clean(ls):
  cmds = []
  for l in ls:
    if l:
      for j, ch in enumerate(l):
        if ch != " ":
          break
      l = l[j:]
      if l[0] != "/":
        l = l.split("//")[0]
        for j, ch in enumerate(reversed(l)):
          if ch != " ":
            break
        cmds.append(l[:len(l) - j])
  return cmds


def translate(cmds):
  asm = ""
  for cmd in cmds:
    asm += parse(cmd) + "\n"
  return asm


if __name__ == "__main__":
  if len(argv) != 3:
    raise RuntimeError("VM translator needs 2 args!")

  inp, out = open(argv[1], "r"), open(argv[2], "w")
  out.write(translate(clean(inp.read().split("\n"))))
