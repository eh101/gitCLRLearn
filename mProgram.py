# -*- coding: gbk -*-
import xlrd
# mPTitle = [
# 'LOAD','LDPC','LDAR','LDIR','LDRi','LDPSW','Rs_B','S2','S1','S0','ALU_B','SW_B','LED_B','RD_D','CS_D','RAM_B','CS_I','ADDR_B','P1','P2','uA5','uA4','uA3','uA2','uA1','uA0']
# print mPTitle

data = xlrd.open_workbook(r'΢ָ��.xls')
# ȡ��0����
table = data.sheets()[0]
# ��ȡ����
nrows = table.nrows
# ��ȡ����
ncols = table.ncols

# д�ļ�
f = open('toVHDL.txt', 'w')

# ��ȡÿ��ÿ�е�����
for i in range(2, nrows):
    # ΢ָ���
    func = '--' + table.cell(i, 0).value
    # ΢��ַ
    mAddr = table.cell(i, 1).value
    # ΢ָ��
    mProgram = []
    for j in range(2, 28):
        mProgram.append(str(table.cell(i, j).value))
    mProgram = "".join(mProgram)
    # VHDL��ʽ
    VHDL = 'WHEN "' + mAddr + '" => DATAOUT<="' + mProgram + '";' + '        ' + func
    print VHDL
    f.write(VHDL.encode('utf-8')+'\n')
f.close()
raw_input()

