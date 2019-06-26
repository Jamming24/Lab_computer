
def load_answer_dict(answer_id_dict_file):
    # 根据长ID 找短ID
    answer_id_dict = dict()
    file_object = open(answer_id_dict_file, 'r', encoding='UTF-8')
    for line in file_object:
        tt = line.split('\t')
        answer_id_dict[tt[1][:32]] = tt[0]
    return answer_id_dict

answer_id_dict_file = "F:\\CCIR_online\\20180809\\answer_id_all.dict"
answer_id_dict = load_answer_dict(answer_id_dict_file)
file_object = open("C:\\Users\\Jamming_Lab\\Desktop\\推荐系统说明文档\\candidate_online.txt", 'r', encoding='UTF-8')
out_fileObject = open("C:\\Users\\Jamming_Lab\\Desktop\\推荐系统说明文档\\candidate_online_shortID.txt", 'w', encoding='UTF-8')
for line in file_object:
    id = line[:32]
    out_fileObject.write('A'+answer_id_dict[id]+'\n')
out_fileObject.close()