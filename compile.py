# -*- coding: gbk -*-
import xlrd
# ==============================
# program default value
# ==============================

# 存储器地址长度，按条件预设
romAddrLen = 8
# 微程序地址长度
mProAddrLen = 6
# 指令中地址长度
addrLen = 8
# PC计数器
pc = 0

# 默认源寄存器，R0
rs = '00'
# 默认目的寄存器，R0
rd = '00'
# 默认地址，00H
addr = ('0' * addrLen)
# 机器指令
bCode = ''

# all file will be used in the program
# asm input filename
asmFilename = 'test.asm'
# controm VHDL filename
conFilename = 'controm.vhd'
# rom VHDL filename
romFilename = 'rom.vhd'
# log filename
logFilename = 'log'
# asm and mProgram design filename
desFilename = 'asm&mp.xls'

# they will create by dynamic
# op table
opTable = {}
# not value op
nOpTable = {}
# single value op
sOpTable = {}
# double value op
dOpTable = {}
# 标号表
markTable = {}

# you can change if you need
# register table
regTable = {
    'R0': '00',
    'R1': '01',
    'R2': '10',
    'R3': '11'
}
# hex2Bin
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


# controm file head
conHead = """LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
ENTITY CONTROM IS
PORT(ADDR: IN STD_LOGIC_VECTOR(5 DOWNTO 0);
     UA:OUT STD_LOGIC_VECTOR(5 DOWNTO 0);
     O:OUT STD_LOGIC_VECTOR(19 DOWNTO 0)
    );
END CONTROM;
ARCHITECTURE A OF CONTROM IS
SIGNAL DATAOUT: STD_LOGIC_VECTOR(25 DOWNTO 0);
BEGIN
    PROCESS
    BEGIN
        CASE ADDR IS
"""

# controm file tail
conTail = """            WHEN OTHERS   => DATAOUT<="10000010001111111100000000";
        END CASE;
        UA(5 DOWNTO 0)<=DATAOUT(5 DOWNTO 0);
        O(19 DOWNTO 0)<=DATAOUT(25 DOWNTO 6);
    END PROCESS;
END A;"""

# rom file head
romHead = """LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.STD_LOGIC_ARITH.ALL;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;
ENTITY ROM IS
PORT(
     DOUT:OUT STD_LOGIC_VECTOR(15 DOWNTO 0);
     ADDR:IN STD_LOGIC_VECTOR(7 DOWNTO 0);
     CS_I:IN STD_LOGIC
);
END ROM;
ARCHITECTURE A OF ROM IS
BEGIN
"""
# rom file tail
romTail = """
           "0000000000000000";
END A;"""


# not op or value
def _empty():
    pass


# 下面为单操作数op分配函数
# 分配的操作数为Rs
def _rs(value):
    # 需使用global声明变量才可修改函数外的变量
    global rs
    rs = value


# 分配的操作数为Rd
def _rd(value):
    global rd
    rd = value


# 分配的操作数为addr
def _addr(value):
    global addr
    addr = value


# 下面为双操作数op分配函数
# 分配的操作数分别为rd和addr
def _da(v1, v2):
    global rd, addr
    rd = v1
    addr = v2


# 分配的操作数分别为rs和rd
def _sd(v1, v2):
    global rs, rd
    rs = v1
    rd = v2


# 分配的操作数分别为rs和addr
def _sa(v1, v2):
    global rs, addr
    rs = v1
    addr = v2


def getOpValueType(i):
    global table
    global nOpTable, sOpTable, dOpTable
    # Rs不为空
    if len(table.cell_value(i, 2)) > 0:
        # Rd不为空
        if len(table.cell_value(i, 3)) > 0:
            # sd型
            dOpTable[table.cell_value(i, 0).encode('ascii')] = _sd
        # addr不为空
        elif len(table.cell_value(i, 4)) > 0:
            # sa型
            dOpTable[table.cell_value(i, 0).encode('ascii')] = _sa
        # Rd为空，addr为空
        else:
            # rs型
            sOpTable[table.cell_value(i, 0).encode('ascii')] = _rs
    # Rs为空，Rd不为空
    elif len(table.cell_value(i, 3)) > 0:
        # addr is empty
        if len(table.cell_value(i, 4)) > 0:
            # da型
            dOpTable[table.cell_value(i, 0).encode('ascii')] = _da
        # Rs and addr is empty
        else:
            # rd
            sOpTable[table.cell_value(i, 0).encode('ascii')] = _rd
    # Rs and Rd is empty, but addr is not empty
    elif len(table.cell_value(i, 4)) > 0:
        # addr
        sOpTable[table.cell_value(i, 0).encode('ascii')] = _addr
    # all is empty
    else:
        nOpTable[table.cell_value(i, 0).encode('ascii')] = _empty


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


# 构建op相关表
def bulidOp(table):
    global opTable
    # 获取行数
    nrows = table.nrows
    # 获取每行每列的数据
    for i in range(4, nrows):
        # op不为空
        if len(table.cell_value(i, 1)) > 0:
            opTable[table.cell_value(i, 0).encode('ascii')] = table.cell_value(i, 1).encode('ascii')
            getOpValueType(i)


# 构建markTable，顺便所有指令转大写
def bulidMarkTable(lines):
    pc = 0
    global markTable
    # 先循环查找生成markTable
    for line in lines:
        # 指令转大写
        line = line.upper()
        # line修改大写内容写回lines
        lines[pc] = line
        if line.find(':') >= 0:
            # 有标号
            # 分离标号和指令
            line = line.split(':')
            # markName = line[0]
            # 将标号及地址存入markTable
            markTable[line[0]] = convAddr(pc)
        # PC计数器+1
        pc += 1
#     分离的标号没有写回lines

# ========================================
# 下面的代码很烂，还没时间整理
# ========================================

xlrd.Book.encoding = "gbk"
data = xlrd.open_workbook(desFilename)
# 取第0个表
table = data.sheets()[0]
bulidOp(table)
# print opTable
# print nOpTable
# print sOpTable
# print dOpTable

# 微指令写入controm.vhd
f = open(conFilename, 'w')
f.write(conHead.encode('utf-8'))
for i in range(4, table.nrows):
    # 微指令功能
    func = '--' + table.cell(i, 0).value
    # 微地址
    mAddr = table.cell(i, 5).value
    # 微指令
    mProgram = []
    for j in range(6, 27):
        mProgram.append(str(table.cell(i, j).value))
    mProgram = "".join(mProgram)
    # VHDL格式
    VHDL = '			WHEN "' + mAddr + '" => DATAOUT<="' + mProgram + '";        ' + func
    f.write(VHDL.encode('utf-8')+'\n')
    # print VHDL
f.write(conTail.encode('utf-8'))
f.close()


# 微指令写入rom.vhd
f = open(romFilename, 'w')
f.write(romHead.encode('utf-8'))
asm = open(asmFilename, 'r+')
lines = asm.readlines()
bulidMarkTable(lines)
for line in lines:
    if line.find(':') >= 0:
        # 有标号
        # 分离标号和指令
        line = line.split(':')
        # 指令
        line = line[1]
    # 每次循环rs,rd,addr，bCode复位
    # 默认源寄存器，R0
    rs = '00'
    # 默认目的寄存器，R0
    rd = '00'
    # 默认地址，00H
    addr = ('0' * addrLen)
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
    if pc==0:
        VHDL='     DOUT<="'+bCode+'" WHEN ADDR="'+convAddr(pc)+'" AND CS_I=\'0\' ELSE        --'
    else:
        VHDL='           "'+bCode+'" WHEN ADDR="'+convAddr(pc)+'" AND CS_I=\'0\' ELSE        --'
    # 注释
    VHDL=VHDL+lines[pc]
    f.write(VHDL.encode('utf-8'))
    # print "bCode:" + bCode, "addr:" + convAddr(pc)  # ,opTable[op],rs,rd,addr
    # PC计数器+1
    pc += 1
f.write(romTail.encode('utf-8'))
f.close()