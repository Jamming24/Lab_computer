# encoding:utf-8
# 输入最大报文长度
x = int(input())
# 输入要插入的报文长度
y = int(input())
# 输入已经存在的报文长度
z = input()
data_long = []
offset = []
for i in range(0, 16):
    if z == 'end':
        break
    else:
        temp = z.split(',')
        offset.append(temp[0])
        data_long.append(temp[1])
        z = input()
index = 0
flag = 0
print_list = []
for every_offset in offset:
    off = int(every_offset)
    long = int(data_long[index])
    if off >= y and (off + long) <= x:
        flag = 1
        off = off-y
        long = off + long
        print_list.append([off, long])
    else:
        print_list.append([off, long])
    index += 1
if flag == 0:
    print_list.append([0, y])
    print(str(print_list[-1][0])+','+str(print_list[-1][1]))
    for j in range(0, len(print_list)-1):
        print(str(print_list[j][0])+','+str(print_list[j][1]))
else:
    for k in print_list:
        print(str(k[0]) + ',' + str(k[1]))
