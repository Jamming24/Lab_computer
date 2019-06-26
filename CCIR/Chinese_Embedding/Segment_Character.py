# -*- coding: UTF-8 -*-

import numpy as np


def Seg_Character():
    simply_wiki_path = "F:\\迅雷下载\\simply_wiki.zh.text"
    Seg_Character = "F:\\迅雷下载\\Seg_Character_simply_wiki.zh.text"
    simply_file_object = open(simply_wiki_path, 'r', encoding="UTF-8")
    Seg_Character_object = open(Seg_Character, 'w', encoding='UTF-8')

    for line in simply_file_object:
        line = line.replace(" ", "").strip("\n")
        new_line = ""
        for chara in line:
            new_line += chara + " "
        Seg_Character_object.write(new_line + "\n")
    simply_file_object.close()
    Seg_Character_object.close()

def Sum_Character_Vector(Seg_Character_Vector_file, Word_Vector_file):
    Charecter_object = open(Seg_Character_Vector_file, 'r', encoding="UTF-8")
    Word_Vector_object = open(Word_Vector_file, 'w', encoding="UTF-8")
    WordS_object = open("F:\\迅雷下载\\Words.txt", 'r', encoding="UTF-8")
    Words  = set()
    for word in WordS_object:
        Words.add(word.strip('\n'))
    # print(Words)
    Character_Vectors = dict()

    size = 0
    for line in Charecter_object:
        ll = line.strip("\n").split(" ")
        character = ll[0]
        size = len(ll) - 2
        vector = ll[1:-1]
        new_vector = np.array(list(map(lambda x: float(x), vector)))
        Character_Vectors[character] = new_vector
    print(len(Character_Vectors))
    Word_Vector_object.write(str(len(Words)) + " "+str(size) + "\n")
    for word in Words:
        print(word)
        Word_Vector_object.write(word + " ")
        sum_vector = np.zeros(size)
        for chara in word:
            temp_vector = Character_Vectors[chara]
            sum_vector += temp_vector
        print(sum_vector)
        for n in sum_vector:
            Word_Vector_object.write(str(round(n, 6))+" ")
        Word_Vector_object.write("\n")
    WordS_object.close()
    Word_Vector_object.close()
    Charecter_object.close()
# Seg_Character()


Seg_Character_Vector_file = "F:\\迅雷下载\\Seg_Character_Vector.txt"
Word_Vector_file = "F:\\迅雷下载\\Seg_Character_Sum_Word_Vector.txt"
Sum_Character_Vector(Seg_Character_Vector_file, Word_Vector_file)
