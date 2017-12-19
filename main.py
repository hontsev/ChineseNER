# -*- coding: utf-8 -*-
import sys
import ner
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("调用方法: python main.py [method] [params]")
        print("-以下是method参数的说明:")
        print("train: 用数据训练CRF模型 (main.py train [filename])")
        print("ner: 用训练好的模型来对输入的文本进行命名实体识别 (main.py ner 北京今天天气真好呀)")
        print("     或者从文件中读取待分析文本，结果输出到文件 (main.py ner -f [origin_filename] [output_filename])")
        print("report: 用给定数据文件进行准确率、召回率、F1值的评估，显示出评估结果(main.py report [filename])")
        exit(0)
    method=sys.argv[1]
    if method == 'train':
        if(len(sys.argv)>=3):
            train_file=sys.argv[2]
            ner.load(train_file=train_file)
        else:
            ner.load()
        ner.train()
    elif method == 'ner':
        if len(sys.argv)>=3 and sys.argv[2]!='-f':
            text=sys.argv[2]
            print(ner.ner(text))
        elif len(sys.argv)>=5 and sys.argv[2]=='-f':
            input_file_path=sys.argv[3]
            output_file_path=sys.argv[4]
            input_file=open(input_file_path,'r',encoding='utf-8')
            result=ner.ner(input_file.read())

            output_file= open(output_file_path,'w',encoding='utf-8')
            try:
                output_file.write(result)
            finally:
                output_file.close()
        else:
            print("格式不对")
    elif method=='report':
        if (len(sys.argv) >= 3):
            test_file = sys.argv[2]
            ner.load(test_file=test_file)
        else:
            ner.load()
        ner.tagger()
