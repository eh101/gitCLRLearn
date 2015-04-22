# -*- coding: gbk -*-
# op��
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
# �Ĵ�����
regTable = {
    'R0': '00',
    'R1': '01',
    'R2': '10',
    'R3': '11'
}
# ʮ������ת������
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

# �ļ���
filename = 'test.asm'
# �洢����ַ���ȣ�������Ԥ��
romAddrLen = 8
# PC������
pc = 0
# ��ű�
markTable = {}

# Ĭ��Դ�Ĵ�����R0
rs = '00'
# Ĭ��Ŀ�ļĴ�����R0
rd = '00'
# Ĭ�ϵ�ַ��00H
addr = ('0' * 8)
# ������
bCode = ''

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

# ��������op�����
sOpTable = {
    'IN1': _rd,
    'INC': _rd,
    'DEC': _rd,
    'JNZ': _addr,
    'JMP': _addr,
    'OUT1': _rs
}
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

# ˫������op�����
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
# ����ΪԤ������
# ========================================================
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

# ������ļ�
asm = open(filename, 'r+')
lines = asm.readlines()
# ��ѭ����������markTable
# print lines
for line in lines:
    # ָ��ת��д
    line = line.upper()
    if line.find(':') >= 0:
        # �б��
        # �����ź�ָ��
        line = line.split(':')
        # markName = line[0]
        # ����ż���ַ����markTable
        markTable[line[0]] = convAddr(pc)
        # ָ��
        line = line[1]
    lines[pc]=line
    # PC������+1
    pc += 1
# PC��λ
pc = 0
print lines
for line in lines:
    # # ָ��ת��д
    # line = line.upper()
    # if line.find(':') >= 0:
    #     # �б��
    #     # �����ź�ָ��
    #     line = line.split(':')
    #     # ָ��
    #     line = line[1]
    #ÿ��ѭ��rs,rd,addr��bCode��λ
    # Ĭ��Դ�Ĵ�����R0
    rs = '00'
    # Ĭ��Ŀ�ļĴ�����R0
    rd = '00'
    # Ĭ�ϵ�ַ��00H
    addr = ('0' * 8)
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
    print "bCode:"+bCode,"addr:"+convAddr(pc)#,opTable[op],rs,rd,addr
    # PC������+1
    pc += 1
