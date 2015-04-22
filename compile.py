# -*- coding: gbk -*-
import xlrd
# ==============================
# program default value
# ==============================

# �洢����ַ���ȣ�������Ԥ��
romAddrLen = 8
# ΢�����ַ����
mProAddrLen = 6
# ָ���е�ַ����
addrLen = 8
# PC������
pc = 0

# Ĭ��Դ�Ĵ�����R0
rs = '00'
# Ĭ��Ŀ�ļĴ�����R0
rd = '00'
# Ĭ�ϵ�ַ��00H
addr = ('0' * addrLen)
# ����ָ��
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
# ��ű�
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


# ����Ϊ��������op���亯��
# ����Ĳ�����ΪRs
def _rs(value):
    # ��ʹ��global���������ſ��޸ĺ�����ı���
    global rs
    rs = value


# ����Ĳ�����ΪRd
def _rd(value):
    global rd
    rd = value


# ����Ĳ�����Ϊaddr
def _addr(value):
    global addr
    addr = value


# ����Ϊ˫������op���亯��
# ����Ĳ������ֱ�Ϊrd��addr
def _da(v1, v2):
    global rd, addr
    rd = v1
    addr = v2


# ����Ĳ������ֱ�Ϊrs��rd
def _sd(v1, v2):
    global rs, rd
    rs = v1
    rd = v2


# ����Ĳ������ֱ�Ϊrs��addr
def _sa(v1, v2):
    global rs, addr
    rs = v1
    addr = v2


def getOpValueType(i):
    global table
    global nOpTable, sOpTable, dOpTable
    # Rs��Ϊ��
    if len(table.cell_value(i, 2)) > 0:
        # Rd��Ϊ��
        if len(table.cell_value(i, 3)) > 0:
            # sd��
            dOpTable[table.cell_value(i, 0).encode('ascii')] = _sd
        # addr��Ϊ��
        elif len(table.cell_value(i, 4)) > 0:
            # sa��
            dOpTable[table.cell_value(i, 0).encode('ascii')] = _sa
        # RdΪ�գ�addrΪ��
        else:
            # rs��
            sOpTable[table.cell_value(i, 0).encode('ascii')] = _rs
    # RsΪ�գ�Rd��Ϊ��
    elif len(table.cell_value(i, 3)) > 0:
        # addr is empty
        if len(table.cell_value(i, 4)) > 0:
            # da��
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


# ConvertAddr��ת����ַΪ������ַ
# addrΪʮ��������
def convAddr(decAddr):
    romAddr = bin(decAddr).replace('0b', '')
    fillLen = romAddrLen - len(romAddr)
    return ('0' * fillLen) + romAddr


# ConvertValue��ת��������Ϊ��������
# valueΪstr
# �ȼ���˳��regTable->hex2Bin->markTable
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


# ����op��ر�
def bulidOp(table):
    global opTable
    # ��ȡ����
    nrows = table.nrows
    # ��ȡÿ��ÿ�е�����
    for i in range(4, nrows):
        # op��Ϊ��
        if len(table.cell_value(i, 1)) > 0:
            opTable[table.cell_value(i, 0).encode('ascii')] = table.cell_value(i, 1).encode('ascii')
            getOpValueType(i)


# ����markTable��˳������ָ��ת��д
def bulidMarkTable(lines):
    pc = 0
    global markTable
    # ��ѭ����������markTable
    for line in lines:
        # ָ��ת��д
        line = line.upper()
        # line�޸Ĵ�д����д��lines
        lines[pc] = line
        if line.find(':') >= 0:
            # �б��
            # �����ź�ָ��
            line = line.split(':')
            # markName = line[0]
            # ����ż���ַ����markTable
            markTable[line[0]] = convAddr(pc)
        # PC������+1
        pc += 1
#     ����ı��û��д��lines

# ========================================
# ����Ĵ�����ã���ûʱ������
# ========================================

xlrd.Book.encoding = "gbk"
data = xlrd.open_workbook(desFilename)
# ȡ��0����
table = data.sheets()[0]
bulidOp(table)
# print opTable
# print nOpTable
# print sOpTable
# print dOpTable

# ΢ָ��д��controm.vhd
f = open(conFilename, 'w')
f.write(conHead.encode('utf-8'))
for i in range(4, table.nrows):
    # ΢ָ���
    func = '--' + table.cell(i, 0).value
    # ΢��ַ
    mAddr = table.cell(i, 5).value
    # ΢ָ��
    mProgram = []
    for j in range(6, 27):
        mProgram.append(str(table.cell(i, j).value))
    mProgram = "".join(mProgram)
    # VHDL��ʽ
    VHDL = '			WHEN "' + mAddr + '" => DATAOUT<="' + mProgram + '";        ' + func
    f.write(VHDL.encode('utf-8')+'\n')
    # print VHDL
f.write(conTail.encode('utf-8'))
f.close()


# ΢ָ��д��rom.vhd
f = open(romFilename, 'w')
f.write(romHead.encode('utf-8'))
asm = open(asmFilename, 'r+')
lines = asm.readlines()
bulidMarkTable(lines)
for line in lines:
    if line.find(':') >= 0:
        # �б��
        # �����ź�ָ��
        line = line.split(':')
        # ָ��
        line = line[1]
    # ÿ��ѭ��rs,rd,addr��bCode��λ
    # Ĭ��Դ�Ĵ�����R0
    rs = '00'
    # Ĭ��Ŀ�ļĴ�����R0
    rd = '00'
    # Ĭ�ϵ�ַ��00H
    addr = ('0' * addrLen)
    # ������
    bCode = ''

    # �����룬����������
    line = line.split()
    # ������
    op = line[0]
    # ������
    line = line[1]
    if line.find(',') >= 0:
        # ˫������
        line = line.split(',')
        v1 = convValue(line[0])
        v2 = convValue(line[1])
        dOpTable[op](v1, v2)
    else:
        # ��������
        value = convValue(line)
        sOpTable[op](value)
    # ��ϻ�������
    bCode = opTable[op] + rs + rd + addr
    if pc==0:
        VHDL='     DOUT<="'+bCode+'" WHEN ADDR="'+convAddr(pc)+'" AND CS_I=\'0\' ELSE        --'
    else:
        VHDL='           "'+bCode+'" WHEN ADDR="'+convAddr(pc)+'" AND CS_I=\'0\' ELSE        --'
    # ע��
    VHDL=VHDL+lines[pc]
    f.write(VHDL.encode('utf-8'))
    # print "bCode:" + bCode, "addr:" + convAddr(pc)  # ,opTable[op],rs,rd,addr
    # PC������+1
    pc += 1
f.write(romTail.encode('utf-8'))
f.close()