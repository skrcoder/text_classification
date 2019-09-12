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
import sys
import codecs
import random

'''
python gen_instance.py sys.argv[1]
sys.argv[1]:分词后的样本:label token_1 token_2...
argv2:输出样本文件
argv3:主题特征文件
argv4:保留的top主题数
argv5:增加了主题特征的新特征文件
'''
feature_dict = {}
#特征从1开始
index = 0
with codecs.open(sys.argv[5], "r", "utf-8") as f_feature:
    for line in f_feature:
        index += 1
        line_inf = line.strip().split("\t")
        id = line_inf[0]
        name = line_inf[1]
        static = line_inf[2]
        feature_dict[name] = id

with codecs.open(sys.argv[3], "r", "utf-8") as f_feature_add:
    feature_toadd = []
    for line in f_feature_add:
        line_inf = line.strip().split(" ", 1)
        #前50个主题,存在主题为空的情况
        if len(line_inf) == 1:
            feature_toadd.append([])
            continue
        value = int(sys.argv[4])
        feature_inf = ["topic_" + temp.split(":")[0] for temp in line_inf[1].split(" ")][:value]
        feature_toadd.append(feature_inf)


with codecs.open(sys.argv[1], "r", "utf-8") as f_in, \
        codecs.open(sys.argv[2], "w", "utf-8") as f_out:
    id = 0
    for line in f_in:
        line_inf = line.strip().split("\t")
        if len(line_inf) != 2:
            print "gen instance err"
            continue
        label = line_inf[0]
        sample = line_inf[1].split(" ")
        feature_id_list = []
        for item in sample:
            if item in feature_dict and int(feature_dict[item]) not in feature_id_list:
                feature_id_list.append(int(feature_dict[item]))
        #增加主题词特征
        for item in feature_toadd[id]:
            if item in feature_dict and int(feature_dict[item]) not in feature_id_list:
                feature_id_list.append(int(feature_dict[item]))
        id += 1
        feature_id_list.sort()
        f_out.write(label + " " + " ".join([str(tmp) + ":1" for tmp in feature_id_list]) + "\n")

print "gen instance of liblinear done"
