# -*- coding: gbk -*-
import xlrd
# mPTitle = [
# 'LOAD','LDPC','LDAR','LDIR','LDRi','LDPSW','Rs_B','S2','S1','S0','ALU_B','SW_B','LED_B','RD_D','CS_D','RAM_B','CS_I','ADDR_B','P1','P2','uA5','uA4','uA3','uA2','uA1','uA0']
# print mPTitle

data = xlrd.open_workbook(r'微指令.xls')
# 取第0个表
table = data.sheets()[0]
# 获取行数
nrows = table.nrows
# 获取列数
ncols = table.ncols

# 写文件
f = open('toVHDL.txt', 'w')

# 获取每行每列的数据
for i in range(2, nrows):
    # 微指令功能
    func = '--' + table.cell(i, 0).value
    # 微地址
    mAddr = table.cell(i, 1).value
    # 微指令
    mProgram = []
    for j in range(2, 28):
        mProgram.append(str(table.cell(i, j).value))
    mProgram = "".join(mProgram)
    # VHDL格式
    VHDL = 'WHEN "' + mAddr + '" => DATAOUT<="' + mProgram + '";' + '        ' + func
    print VHDL
    f.write(VHDL.encode('utf-8')+'\n')
f.close()
raw_input()

