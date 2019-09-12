#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: feature_add.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2017/08/24 12:13:07
"""
import codecs
import sys
'''
argv1:需要增加的主题特征文件
argv2:需要保留的top主题个数
argv3:原来特征文件
argv4:新的特征文件
'''

with codecs.open(sys.argv[1], "r", "utf-8") as f_in, \
        codecs.open(sys.argv[3], "r", "utf-8") as feature,\
        codecs.open(sys.argv[4], "w", "utf-8") as f_out:
    id = 0
    for line in feature:
        f_out.write(line)
        id += 1
    id += 1
    feature_toadd = {}
    for line in f_in:
        line_inf_tmp = line.strip().split(" ", 1)
        if len(line_inf_tmp) != 2:
            print "no topic", line,
            continue
        line_inf = line_inf_tmp[1]
        #取前value个主题
        value = int(sys.argv[2])
        feature_id = ["topic_" + tmp.split(":")[0] for tmp in line_inf.split(" ")][:value]
        for item in feature_id:
            feature_toadd[item] = feature_toadd.get(item, 0) + 1
    sorted_feature = sorted(feature_toadd.items(), key = lambda x: x[1], reverse = True)
    for item in sorted_feature:
        f_out.write(str(id) + "\t" + item[0] + "\t" + str(item[1]) + "\n")
        id += 1

print "add new feature done"
        


