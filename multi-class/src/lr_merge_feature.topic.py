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
import sys
import codecs

"""
python lr_porn.model_merge_feature.py argv1 argv2 argv3
argv1:modle文件
argv2:feature文件
argv3:输出文件
"""

with codecs.open(sys.argv[1], "r", "utf-8") as f_result:
    result = [tmp.strip() for tmp in f_result.readlines()[6:]]

with codecs.open(sys.argv[2], "r", "utf-8") as f_in, \
        codecs.open(sys.argv[3], "w", "utf-8") as f_out:
    id = 0
    result_dict ={}
    for line in f_in:
        result_dict[line.strip()] = float(result[id])
        id += 1
    sorted_result = sorted(result_dict.items(), key = lambda x:x[1], reverse = True)
    for item in sorted_result:
        f_out.write(item[0] + "\t" + str(item[1]) + "\n")

print "feature merge done"

