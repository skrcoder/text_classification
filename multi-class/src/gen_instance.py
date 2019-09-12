#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: gen_instance.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2017/08/01 19:24:17
"""
import os
import sys
import codecs
import random

'''
python gen_instance.py argv[1] argv[2]
argvs:
argv[1]:数据基目录路径,该目录下文件：baimingdan, feature, model
argv[2]:分词后的样本路径:label token_1 token_2...
argv[2]:输出的样本路径
output:
    得到样本作为模型的输出
'''
feature_file_path = sys.argv[1]
input_file_path = sys.argv[2]
output_file_path = sys.argv[3]

feature_dict = {}
#特征从1开始
with codecs.open(feature_file_path, "r", "utf-8") as f_feature:
    for line in f_feature:
        line_inf = line.strip().split("\t")
        id = line_inf[0]
        name = line_inf[1]
        static = line_inf[2]
        feature_dict[name] = id

with codecs.open(input_file_path, "r", "utf-8") as f_in, \
        codecs.open(output_file_path, "w", "utf-8") as f_out:
    id = 0
    for line in f_in:
        id += 1
        line_inf = line.strip().split("\t")
        if len(line_inf) != 2:
            print "gen instance err: ", str(id)
            sys.exit(0)
        label = line_inf[0]
        sample = line_inf[1].split(" ")
        feature_id_list = []
        for item in sample:
            if item in feature_dict and int(feature_dict[item]) not in feature_id_list:
                feature_id_list.append(int(feature_dict[item]))
        feature_id_list.sort()
        f_out.write(label + " " + " ".join([str(tmp) + ":1" for tmp in feature_id_list]) + "\n")

print "gen instance of liblinear done"

