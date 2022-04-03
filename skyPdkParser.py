import re
import sys
import logging


def replaceTextInFile(line, lines, sourceText, destinationText):
    if line.__contains__(sourceText):
        pos = lines.index(line)
        lines.remove(line)
        line = line.replace(sourceText, destinationText)
        lines.insert(pos, line)
    return line

def includeSkyLib(line,lines,flag):
    if line.__contains__('.include PMOS-180nm.lib') and flag == 0:
        line = replaceTextInFile(line, lines, '.include PMOS-180nm.lib', '.lib "sky130_fd_pr/models/sky130.lib.spice" tt')
        flag = 1
    elif line.__contains__('.include NMOS-180nm.lib') and flag == 1:
        line = replaceTextInFile(line, lines, '.include NMOS-180nm.lib', ' ')
    elif line.__contains__('.include NMOS-180nm.lib') and flag == 0:
        line = replaceTextInFile(line, lines, '.include NMOS-180nm.lib', '.lib "sky130_fd_pr/models/sky130.lib.spice" tt')
        flag = 1
    else:
        line = replaceTextInFile(line, lines, '.include PMOS-180nm.lib', ' ')
    return flag, line

def replaceMosfetLabel(line, lines):
    mos = re.search(r'\Am\d+ ', line)
    if mos!= None:
        mosxm = mos.group().replace('m','xm')
        line = replaceTextInFile(line,lines,mos.group(),mosxm)
    return line

def configurePmosWbyL(line, lines, width, length):
    mos = re.search(r'CMOSP [w,W]=\d+\.*\d*[a-z] [l,L]=\d+\.*\d*[a-z] [m,M]=\d', line)
    if mos!= None:
        pmos = 'sky130_fd_pr__pfet_01v8 W='+ width + ' L='+ length
        line = replaceTextInFile(line,lines,mos.group(),pmos)
    return line

def configureNmosWbyL(line, lines, width, length):
    mos = re.search(r'CMOSN [w,W]=\d+\.*\d*[a-z] [l,L]=\d+\.*\d*[a-z] [m,M]=\d', line)
    if mos!= None:
        nmos = 'sky130_fd_pr__nfet_01v8 W=' + width + ' L=' + length
        line = replaceTextInFile(line,lines,mos.group(),nmos)
    return line

logging.basicConfig(format='%(message)s', level=logging.DEBUG)
logger = logging.getLogger()

filename = input("Enter the File Name which needs to be parsed: ")

try:
    with open(filename, 'r') as a:
        b = a.readlines()
except:
    logger.error("FILE NOT FOUND!!")
    sys.exit()

wantToEnterWidthOrLength = input("Do you want to enter Length and Width of MOSFETS?(Y/N): ")

if wantToEnterWidthOrLength == 'y' or wantToEnterWidthOrLength == 'Y':
    pwidth = input("Enter the Width for PMOS: ")
    plength = input("Enter the Length for PMOS: ")
    nwidth = input("Enter the Width for NMOS: ")
    nlength = input("Enter the Length for NMOS: ")
elif wantToEnterWidthOrLength == 'n' or wantToEnterWidthOrLength == 'N':
    pwidth = '1.29'
    plength = '0.18'
    nwidth = '0.5'
    nlength = '0.18'
else:
    logger.error("Invalid input entered!!")
    sys.exit()

try:
    with open(filename, 'r+') as f:
        lines = f.readlines()
        flag = 0
        for line in lines:
            flag, line = includeSkyLib(line,lines,flag)
            line = replaceMosfetLabel(line,lines)
            line = configurePmosWbyL(line, lines, pwidth, plength)
            line = configureNmosWbyL(line, lines, nwidth, nlength)
        f.seek(0)
        f.writelines(lines)
    logger.info("FILE CONVERTED SUCCESSFULLY!!")
except:
    logger.error("Error Occurred!! Please check your File!!")



