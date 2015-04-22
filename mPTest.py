# -*- coding: gbk -*-
import xlrd
# mPTitle = [
# 'LOAD','LDPC','LDAR','LDIR','LDRi','LDPSW','Rs_B','S2','S1','S0','ALU_B','SW_B','LED_B','RD_D','CS_D','RAM_B','CS_I','ADDR_B','P1','P2','uA5','uA4','uA3','uA2','uA1','uA0']
# print mPTitle

# 默认源寄存器，R0
rs = '00'
# 默认目的寄存器，R0
rd = '00'
# 默认地址，00H
addr = ('0' * 8)


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
    # 需使用global声明变量才可修改函数外的变量
    global rd
    rd = value


# 分配的操作数为addr
def _addr(value):
    global addr
    addr = value


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


def testOp(i):
    global table
    global nOpTable,sOpTable,dOpTable
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

xlrd.Book.encoding = "gbk"
data = xlrd.open_workbook('asm&mp.xls')
# 取第0个表
table = data.sheets()[0]
# 获取行数
nrows = table.nrows
# 获取列数
ncols = table.ncols
print 'nrows:', nrows, 'ncols:', ncols
# 写文件
# f = open('toVHDL.txt', 'w')
opTable = {}
sOpTable = {}
dOpTable = {}
nOpTable={}
# 获取每行每列的数据
for i in range(4, nrows):
    # op不为空
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
# # 微指令功能
# func = '--' + table.cell(i, 0).value
#     # 微地址
#     mAddr = table.cell(i, 1).value
#     # 微指令
#     mProgram = []
#     for j in range(2, 28):
#         mProgram.append(str(table.cell(i, j).value))
#     mProgram = "".join(mProgram)
#     # VHDL格式
#     VHDL = 'WHEN "' + mAddr + '" => DATAOUT<="' + mProgram + '";' + '        ' + func
#     print VHDL
#     f.write(VHDL.encode('utf-8')+'\n')
# f.close()
