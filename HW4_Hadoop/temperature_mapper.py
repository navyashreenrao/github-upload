import sys

for line in sys.stdin:
    line = line.strip()
    temperature = int(line[87:92])
    quality = int(line[92])
    quality_list = [0,1,4,5,9]
    if ((temperature != 9999) and (quality in quality_list)):
        print('%s\t%d' % (line[15:23], int(line[87:92])))