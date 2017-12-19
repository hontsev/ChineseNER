# -*- coding: utf-8 -*-

# 将统一化的输入数据格式化为list
def format_data1():
    res=list()
    res_line=list()
    tmp=load_data('weiboNER.conll.train')
    for line in tmp:
        tmpres=line.replace('\n','').split('\t')
        if(tmpres.__len__()<2):
            res.append(res_line)
            res_line=list()
            continue
        # print(tmpres)
        d1=tmpres[0]
        d2=tmpres[1]
        if(d2.split('.').__len__()>=2):
            d2=d2.split('.')[0]
        res_line.append((d1,d2))
    # res.append(res_line)
    print(res)

# 将boson的数据中的实体名转化为标准实体名
def get_type(text):
    if text.__contains__('product_name'):
        return 'PRO'
    elif text.__contains__('person_name'):
        return 'PER'
    elif text.__contains__('time'):
        return 'TIM'
    elif text.__contains__('org_name'):
        return 'ORG'
    elif text.__contains__('company_name'):
        return 'ORG'
    elif text.__contains__('location'):
        return 'LOC'
    else:
        return 'O'

def get_type_encode(text):
    if text.__contains__('PRO'):
        return 'product_name'
    elif text.__contains__('PER'):
        return 'person_name'
    elif text.__contains__('TIM'):
        return 'time'
    elif text.__contains__('ORG'):
        return 'org_name'
    elif text.__contains__('LOC'):
        return 'location'
    else:
        return 'unknown'

# 将boson数据格式归一化为系统内部的格式
def format_boson_data(file_name='corpus/BosonNLP_NER_6C.txt'):
    res=list()
    tmp = load_data(file_name)
    for line in tmp:
        state=0
        lastc=''
        ename=""

        for c in line:
            if c=='{' and state==0:
                state=1
            elif c=='{' and lastc=='{' and state==1:
                state=2
            elif c==':' and state==2:
                state=3
            elif c=='}' and state==4:
                state=5
            elif c=='}' and lastc=='}' and state==5:
                state=0
            elif state==0 and c!=' ' and c!='\n':
                res.append(c+" O")
            elif state==2:
                ename+=c
            elif state==3 and c!=' ':
                ename=get_type(ename)
                res.append(c+" B-"+ename)
                state=4
            elif state==4:
                res.append(c + " I-" + ename)
            lastc=c
        res.append("")
    print(res)
    # save
    file=open("corpus/boson_ner_format.txt",'w',encoding='utf-8')
    try:
        # file.writelines(res)
        for item in res:
            file.write(item+"\n")
            # file.write("\r\n")
            # print("\r")
    finally:
        file.close()

# 输出按boson语料的格式规范化后的命名实体标记
def format_boson_data_encode(text,tag):
    res=""
    status=0
    for i in range(len(text)):
        if status == 0 and tag[i] == 'O':
            res += text[i]
        elif status == 0 and tag[i] != 'O':
            status = 1
            res += "{{" + get_type_encode(tag[i]) + ":" + text[i]
        elif status == 1 and str(tag[i]).startswith('I'):
            res += text[i]
        elif status == 1:
            res += "}}"
            if tag[i] == 'O':
                status = 0
                res += text[i]
            else:
                status = 1
                res += "{{" + get_type_encode(tag[i]) + ":" + text[i]
    return res



import jieba.posseg as jbpos
# import jieba.analyse as jbal

# 为token填充分词标记和词性标记
def get_cut_and_seg(token):
    wordlist = jbpos.cut(get_sentence(token))
    res = list()
    index=0
    for w in wordlist:
        for i in range(len(w.word)):
            if len(w.word) == 1:
                status = 'S'
            elif i == 0:
                status = 'B'
            elif i == len(w.word) - 1:
                status = 'E'
            else:
                status = 'I'
            token[index][1]=status
            token[index][2]=w.flag
            index += 1
    return res

# 把token序列组合成原句
def get_sentence(token):
    sentence= ''
    for t in token:
        sentence += t[0]
    return sentence

# 读入数据
def load_data(path):
    file=open(path,'r',encoding='utf-8')
    res=list()
    try:

        lines=file.readlines()
        # print(lines)
        res_line=list()
        for item in lines:
            if item.split(' ').__len__()>=2:
                word=item.split(' ')[0]
                type=item.split(' ')[1].replace('\n','').replace('\r','')
                res_line.append([word,'','',type])
            else:
                get_cut_and_seg(res_line)
                res.append(res_line)
                res_line=list()
    finally:
        file.close()
        # print(res)
    return res

# 将句子切分为一个一个的字，用于输入实体识别
def split_by_words(sentence):
    res=list()
    for word in sentence:
        res.append([word,'','',''])
    get_cut_and_seg(res)
    return res


if __name__ == '__main__':
    # load()
    # train()
    # tagger()
    print(split_by_words('洗衣机，国内掀起了大数据、云计算的热潮。仙鹤门地区。'))