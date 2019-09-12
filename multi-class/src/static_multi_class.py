#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2018 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: static_multi_class.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2018/01/30 17:56:46
"""

'''
按照label的种类生成相应的预测结果
'''

import sys
import codecs

with codecs.open(sys.argv[1], "r", "utf-8") as f_in:
    lables_str_list = f_in.readlines()[0].strip().split("\t")[1:]

for item in lables_str_list:
    label_str = item
    result = {}
    with codecs.open(sys.argv[1], "r", "utf-8") as f_in:
        for index, line in enumerate(f_in):
            if index == 0:
                continue
            line_inf = line.strip().split("\t")
            true_label = line_inf[0]
            predict_label = line_inf[2]
            confident = line_inf[3]
            if predict_label == label_str:
                result[line] = confident
        sorted_result = sorted(result.items(), key = lambda x: -float(x[1]))
    with codecs.open(sys.argv[2]+label_str, "w", "utf-8") as f_out:
        for item in sorted_result:
            f_out.write(item[0])
    
