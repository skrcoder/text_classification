# 项目名称
基于liblinear实现的文本分类工具，支持特征选择，特征增加，多分类，准召评估。在尽量保留更多的中间数据的同时，能分别输出每一个分类的模型特征权重，帮助模型调试。

## 环境配置
1. 需要安装sklearn库（支持特征选择）：pip install sklearn。
2. 下载分词库，并解压在当前目录下。
3. 下载liblinear工具，并解压在当前目录下.
4. 修改conf/conf.sh 中的环境配置路径  

## 快速开始
模型训练：sh bin/run_main.sh train
模型预测：sh bin/run_main.sh test 
