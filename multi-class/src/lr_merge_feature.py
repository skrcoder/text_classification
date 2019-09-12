#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: lr_porn.model_merge_feature.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2017/08/01 21:38:37
"""
import os
import sys
import codecs

"""
python lr_porn.model_merge_feature.py argv1 argv2 argv3
argvs:
argv1:modle文件
argv2:feature文件
argv3:output

"""

with codecs.open(sys.argv[1], "r", "utf-8") as f_result:
    labels, result  = [], []
    for index, content in enumerate(f_result):
        if index == 2:
            labels = content.strip().split()[1:]
        if index > 5:
            result.append(content.strip().split())

with codecs.open(sys.argv[2], "r", "utf-8") as f_in:
    result_dict ={}
    if len(labels) > 2:
        for label_index in range(len(labels)):
            with codecs.open(sys.argv[3]+labels[label_index], "w", "utf-8") as f_out:
                for index, line in enumerate(f_in):
                    result_dict[line.strip()] = float(result[index][label_index])
            sorted_result = sorted(result_dict.items(), key = lambda x:x[1], reverse = True)
            for temp in sorted_result:
                f_out.write(temp[0] + "\t" + str(temp[1]) + "\n")
            f_in.seek(0)
    f_in.seek(0)
    with codecs.open(sys.argv[3]+".all", "w", "utf-8") as f_out:
        result_dict = {}
        for index, line in enumerate(f_in):
            result_dict[line.strip()] = " ".join(result[index])
        sorted_result = sorted(result_dict.items(), key = lambda x:x[1], reverse = True)
        for item in sorted_result:
            f_out.write(item[0] + "\t" + str(item[1]) + "\n")

print "feature merge done"

