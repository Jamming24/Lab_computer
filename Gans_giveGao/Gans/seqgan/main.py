# -*- coding:utf-8 -*-
import getopt
import sys
import nltk
from seqgan.Seqgan import Seqgan
from colorama import Fore

# def set_gan():
#     gan = Seqgan()
#     # gan.vocab_size = 5000
#     # gan.generate_num = 10000
#     # gan.vocab_size = 100
#     # gan.generate_num = 100
#     return gan
# def set_traing(gan, training_method):
#     try:
#         if training_method == 'oracle':
#             gan_func = gan.train_oracle
#         elif training_method == 'cfg':
#             gan_func = gan.train_cfg
#         elif training_method == 'real':
#             gan_func = gan.train_real
#         else:
#             print(Fore.RED + 'Unsupported training setting: ' + training_method + Fore.RESET)
#     except AttributeError:
#         print(Fore.RED + 'Unsupported training setting: ' + training_method + Fore.RESET)
#     return gan_func

if __name__ =='__main__':
    # import nltk
    # nltk.download('punkt')
    # nltk.download()
    gan = Seqgan()
    # train_model = 'real'  # oracle    cfg     real
    # local_data = 'data/en_demo2.txt'
    local_data = 'data/quora_50K_train.txt'
    gan.train_real(local_data)






