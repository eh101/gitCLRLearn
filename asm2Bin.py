# -*- coding: gbk -*-
# op表
opTable = {
    'IN1': '0001',
    'MOV': '0010',
    'LAD': '0011',
    'ADD': '0100',
    'INC': '0101',
    'DEC': '0110',
    'JNZ': '0111',
    'STO': '1000',
    'JMP': '1001',
    'OUT1': '1010',
    'STOI': '1011',
    'SADD': '1100',
    'AND': '1101'
}
# 寄存器表
regTable = {
    'R0': '00',
    'R1': '01',
    'R2': '10',
    'R3': '11'
}
# 十六进制转二进制
hex2Bin = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111'
}

# 文件名
filename = 'test.asm'
# 存储器地址长度，按条件预设
romAddrLen = 8
# PC计数器
pc = 0
# 标号表
markTable = {}

# 默认源寄存器，R0
rs = '00'
# 默认目的寄存器，R0
rd = '00'
# 默认地址，00H
addr = ('0' * 8)
# 机器码
bCode = ''

# 下面为单操作数op分配函数
# 分配的操作数为Rs
def _rs(value):
    # 需使用global声明变量才可修改函数外的变量
    global rs
    rs = value


# 分配的操作数为Rd
def _rd(value):
    # 需使用global声明变量才可修改函数外的变量
    global rd
    rd = value


# 分配的操作数为addr
def _addr(value):
    global addr
    addr = value

# 单操作数op分配表
sOpTable = {
    'IN1': _rd,
    'INC': _rd,
    'DEC': _rd,
    'JNZ': _addr,
    'JMP': _addr,
    'OUT1': _rs
}
# 下面为双操作数op分配函数
# 分配的操作数分别为rd和addr
def _da(v1, v2):
    global rd
    global addr
    rd = v1
    addr = v2


# 分配的操作数分别为rs和rd
def _sd(v1, v2):
    global rs
    global rd
    rs = v1
    rd = v2


# 分配的操作数分别为rs和addr
def _sa(v1, v2):
    global rs
    global addr
    rs = v1
    addr = v2

# 双操作数op分配表
dOpTable = {
    'MOV': _da,
    'LAD': _sd,
    'ADD': _sd,
    'STO': _sa,
    'STOI': _sd,
    'SADD': _sd,
    'AND': _sd
}

# ========================================================
# 以上为预设内容
# ========================================================
# ConvertAddr，转换地址为定长地址
# addr为十进制整数
def convAddr(decAddr):
    romAddr = bin(decAddr).replace('0b', '')
    fillLen = romAddrLen - len(romAddr)
    return ('0' * fillLen) + romAddr


# ConvertValue，转换操作数为机器编码
# value为str
# 先检索顺序regTable->hex2Bin->markTable
def convValue(value):
    code = '0'
    try:
        code = regTable[value]
    except Exception:
        try:
            code = hex2Bin[value[0]] + hex2Bin[value[1]]
        except Exception:
            try:
                code = markTable[value]
            except Exception:
                pass
    finally:
        return code

# 读汇编文件
asm = open(filename, 'r+')
lines = asm.readlines()
# 先循环查找生成markTable
# print lines
for line in lines:
    # 指令转大写
    line = line.upper()
    if line.find(':') >= 0:
        # 有标号
        # 分离标号和指令
        line = line.split(':')
        # markName = line[0]
        # 将标号及地址存入markTable
        markTable[line[0]] = convAddr(pc)
        # 指令
        line = line[1]
    lines[pc]=line
    # PC计数器+1
    pc += 1
# PC复位
pc = 0
print lines
for line in lines:
    # # 指令转大写
    # line = line.upper()
    # if line.find(':') >= 0:
    #     # 有标号
    #     # 分离标号和指令
    #     line = line.split(':')
    #     # 指令
    #     line = line[1]
    #每次循环rs,rd,addr，bCode复位
    # 默认源寄存器，R0
    rs = '00'
    # 默认目的寄存器，R0
    rd = '00'
    # 默认地址，00H
    addr = ('0' * 8)
    # 机器码
    bCode = ''

    # 操作码，操作数分离
    line = line.split()
    # 操作码
    op = line[0]
    # 操作数
    line = line[1]
    if line.find(',') >= 0:
        # 双操作数
        line = line.split(',')
        v1 = convValue(line[0])
        v2 = convValue(line[1])
        dOpTable[op](v1, v2)
    else:
        # 单操作数
        value = convValue(line)
        sOpTable[op](value)
    # 组合机器代码
    bCode = opTable[op] + rs + rd + addr
    print "bCode:"+bCode,"addr:"+convAddr(pc)#,opTable[op],rs,rd,addr
    # PC计数器+1
    pc += 1
