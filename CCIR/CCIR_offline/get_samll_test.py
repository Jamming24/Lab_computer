# encoding:utf-8


def get_small_test():
    flagPath = "E:\\CCIR\\flag.txt"
    test_file = "E:\\CCIR\\available_new_testing_set.txt"
    small_test = "E:\\CCIR\\small_testing_set.txt"
    flag_list = []
    test_file_list = []
    Outlist = []
    flags_object = open(flagPath, 'r', encoding='UTF-8')
    test_file_object = open(test_file, 'r', encoding='UTF-8')
    Out_file_object = open(small_test, 'w', encoding='UTF-8')
    for line in test_file_object:
        test_file_list.append(line)

    for line in flags_object.readlines():
        flag_list.append(line[:1])
    print(f"flag标志：{len(flag_list)}")
    print(f"测试数据集数量{len(test_file_list)}行")
    for i in range(0, len(flag_list)):
        if flag_list[i] == '1':
            Outlist.append(test_file_list[i])

    flags_object.close()
    print(f"最后的小数据集数量:{len(Outlist)}行")

    for index in Outlist:
        Out_file_object.write(index + "\n")
    Out_file_object.close()


def difference():
    small_test = "E:\\CCIR\\small_testing_set.txt"
    office_test = "E:\\testing_set_135089.txt"
    small_test_object = open(small_test, 'r', encoding='UTF-8')
    office_test_object = open(office_test, 'r', encoding='UTF-8')
    office_test_list = []
    small_test_list = []
    for li in small_test_object:
        small_test_list.append(li.split('\t')[1])
    for line in office_test_object:
        office_test_list.append(line.split("\t")[1])
    count = 0
    print(len(office_test_list))
    print(len(small_test_list))
    for i in range(len(office_test)):
        count += 1
        if small_test_list[i] != office_test_list[i]:
            print(small_test_list[i])

    small_test_object.close()
    office_test_object.close()


difference()
