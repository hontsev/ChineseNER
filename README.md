# 一 运行说明
### 1.1 运行环境
本项目开发语言为python，运行环境为python 3.6，依赖库为：
-	Python-crfsuite
-	Sklearn
-	Jieba

项目源代码已放在本人的Github上，地址为 https://github.com/hontsev/ChineseNER

### 1.2 简介
本项目是一个主要采用条件随机场（CRF）进行命名实体识别的程序，可用于自然语言图谱从非结构化数据中抽取命名实体等任务。分别识别人名、地名、组织名这三类实体。
项目采用 `python-crfsuite` 库来进行CRF运算，为了构建文本的词边界、词性特征，采用了 `jieba` 库来进行分词和词性标注。

训练及测试数据来自BosonNLP公开的命名实体标注数据以及一个来自网络的中文命名实体标注数据（https://github.com/crownpku/Small-Chinese-Corpus/tree/master/NER_chi），在此对数据提供者表示感谢。

### 1.3 使用
入口文件为 `main.py` ，调用方法为： `python main.py [method] [params]`

以下是 `method` 参数的说明：

- train：用数据训练CRF模型 (例如：`python main.py train [filename]`)
- ner： 用训练好的模型来对输入的文本进行命名实体识别 (例如：`python main.py ner 北京今天天气真好呀`)；或者从文件中读取待分析文本，结果输出到文件 (例如：`python main.py ner -f [origin_filename] [output_filename]`)
- report： 用给定数据文件进行准确率、召回率、F1值的评估，显示出评估结果(例如：`python main.py report [filename]`)

以下是使用示例：

1. 安装好项目的依赖库，并定位至项目根目录（有 `main.py` 的路径）

2. 训练模型：`python main.py train`
 
默认进行50轮迭代，由于对于数据要进行现场的分词和词性标注，所以训练前的预处理过程可能需要较长时间。
 
3. 等待训练完毕，可用测试集进行性能测试：`python main.py report`
 
4. 进行句子的命名实体识别：`python main.py ner 今天纽约的天气真好啊，京华大酒店的张尧经理吃了一只北京烤鸭。`
 
5. 进行文件的命名实体识别，读入utf-8编码格式的文本文件，输出命名实体识别结果到指定文件内：`python main.py ner -f test/input.txt test/output.txt` 打开指定的输出文件，可见识别结果
 
# 二 性能说明

对LOC、ORG和PER三类命名实体的识别分别进行准确率、召回率和F1值的计算，结果如下：

|     	|	precision	|	recall	|	f1-score	|	support|	
|	 - |	 - |	 -|	-|	-|	
|	B-LOC |		0.88	|	0.84	|	0.86	|	3658|	
|	I-LOC	|	0.84	|	0.84	|	0.84	|	4948|	
|	B-ORG	|	0.84	|	0.72	|	0.78	|	2185|	
|	I-ORG	|	0.86	|	0.78	|	0.82	|	8756|	
|	B-PER	|	0.92	|	0.86	|	0.89	|	1864|	
|	I-PER	|	0.92	|	0.89	|	0.90	|	3601|	
|	avg / total|		0.87	|	0.82	|	0.84	|	25012|	

参考张祝玉等（2008）的论文[1]，我们按照字级，加入了词语边界和词性标注的特征后，整体F1值达到0.84，接近此文所述的0.866的F1值，而人名识别的F1值接近0.9，是三种命名实体中识别效果最好的。

更高级的特征由于性能提升不大或未能收集到相应数据（实体列表等），因此未能充分加入，再加上Jieba分词、词性标注过程中的误差在CRF中的累积，因此本项目的F1值并未达到最高，仍有提升空间。



[1] 张祝玉, 任飞亮, 朱靖波. 基于条件随机场的中文命名实体识别特征比较研究 [C]: 第 4 届全国信息检索与内容安全学术会议论文集. 2008.
