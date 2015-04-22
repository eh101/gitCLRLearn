# -*- coding: gbk -*-
import xlrd
# mPTitle = [
# 'LOAD','LDPC','LDAR','LDIR','LDRi','LDPSW','Rs_B','S2','S1','S0','ALU_B','SW_B','LED_B','RD_D','CS_D','RAM_B','CS_I','ADDR_B','P1','P2','uA5','uA4','uA3','uA2','uA1','uA0']
# print mPTitle

# Ĭ��Դ�Ĵ�����R0
rs = '00'
# Ĭ��Ŀ�ļĴ�����R0
rd = '00'
# Ĭ�ϵ�ַ��00H
addr = ('0' * 8)


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
    # ��ʹ��global���������ſ��޸ĺ�����ı���
    global rd
    rd = value


# ����Ĳ�����Ϊaddr
def _addr(value):
    global addr
    addr = value


# ����Ϊ˫������op���亯��
# ����Ĳ������ֱ�Ϊrd��addr
def _da(v1, v2):
    global rd
    global addr
    rd = v1
    addr = v2


# ����Ĳ������ֱ�Ϊrs��rd
def _sd(v1, v2):
    global rs
    global rd
    rs = v1
    rd = v2


# ����Ĳ������ֱ�Ϊrs��addr
def _sa(v1, v2):
    global rs
    global addr
    rs = v1
    addr = v2


def testOp(i):
    global table
    global nOpTable,sOpTable,dOpTable
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

xlrd.Book.encoding = "gbk"
data = xlrd.open_workbook('asm&mp.xls')
# ȡ��0����
table = data.sheets()[0]
# ��ȡ����
nrows = table.nrows
# ��ȡ����
ncols = table.ncols
print 'nrows:', nrows, 'ncols:', ncols
# д�ļ�
# f = open('toVHDL.txt', 'w')
opTable = {}
sOpTable = {}
dOpTable = {}
nOpTable={}
# ��ȡÿ��ÿ�е�����
for i in range(4, nrows):
    # op��Ϊ��
    if len(table.cell_value(i, 1)) > 0:
        opTable[table.cell_value(i, 0).encode('ascii')] = table.cell_value(i, 1).encode('ascii')
        testOp(i)

print opTable
print nOpTable
print sOpTable
print dOpTable
# for j in range(0, ncols):
# print table.cell_value(i, j),
# print
# # ΢ָ���
# func = '--' + table.cell(i, 0).value
#     # ΢��ַ
#     mAddr = table.cell(i, 1).value
#     # ΢ָ��
#     mProgram = []
#     for j in range(2, 28):
#         mProgram.append(str(table.cell(i, j).value))
#     mProgram = "".join(mProgram)
#     # VHDL��ʽ
#     VHDL = 'WHEN "' + mAddr + '" => DATAOUT<="' + mProgram + '";' + '        ' + func
#     print VHDL
#     f.write(VHDL.encode('utf-8')+'\n')
# f.close()
