
import math


def gen_pfdict(self, f):
    # 初始化前缀词典
    lfreq = {}
    ltotal = 0
    # f_name = resolve_filename(f)
    f_name = "文件"
    for lineno, line in enumerate(f, 1):
        try:
            # 解析离线词典文本文件，离线词典文件格式如第2章中所示
            line = line.strip().decode('utf-8')
            # 词和对应的词频
            word, freq = line.split(' ')[:2]
            freq = int(freq)
            lfreq[word] = freq
            ltotal += freq
            # 获取该词所有的前缀词
            for ch in range(len(word)):
                wfrag = word[:ch + 1]
                # 如果某前缀词不在前缀词典中，则将对应词频设置为0，
                # 如第2章中的例子“北京大”
                if wfrag not in lfreq:
                    lfreq[wfrag] = 0
        except ValueError:
            raise ValueError('invalid dictionary entry in %s at Line %s: %s' % (f_name, lineno, line))
    f.close()
    return lfreq, ltotal


def get_DAG(self, sentence):
    # 检查系统是否已经初始化
    self.check_initialized()
    # DAG存储向无环图的数据，数据结构是dict
    DAG = {}
    N = len(sentence)
    # 依次遍历文本中的每个位置
    for k in range(N):
        tmplist = []
        i = k
        # 位置k形成的片段
        frag = sentence[k]
        # 判断片段是否在前缀词典中
        # 如果片段不在前缀词典中，则跳出本循环
        # 也即该片段已经超出统计词典中该词的长度
        while i < N and frag in self.FREQ:
            # 如果该片段的词频大于0
            # 将该片段加入到有向无环图中
            # 否则，继续循环
            if self.FREQ[frag]:
                tmplist.append(i)
            # 片段末尾位置加1
            i += 1
            # 新的片段较旧的片段右边新增一个字
            frag = sentence[k:i + 1]
        if not tmplist:
            tmplist.append(k)
        DAG[k] = tmplist
    return DAG

def calc(self, sentence, DAG, route):
    N = len(sentence)
    # 初始化末尾为0
    route[N] = (0, 0)
    logtotal = math.log(self.total)
    # 从后到前计算
    for idx in range(N - 1, -1, -1):
        route[idx] = max((math.log(self.FREQ.get(sentence[idx:x + 1]) or 1) -
                            logtotal + route[x + 1][0], x) for x in DAG[idx])
