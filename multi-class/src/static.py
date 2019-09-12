#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: test.data.wordseg.out.result.merge.static.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2017/08/02 22:11:20
"""
import sys
import codecs

'''
python test.data.wordseg.out.result.merge.static.py argv1
argv1:merge后的数据: true_label\tcontent\tpredict_label\tprobability
argv:输出文件
'''
with codecs.open(sys.argv[1], "r", "utf-8") as f_in:
    lables_str_list = f_in.readlines()[0].strip().split("\t")[1:]

for item in lables_str_list:
    label_str = item
    with codecs.open(sys.argv[1], "r", "utf-8") as f_in:
        true_inf = {"P": 0, "N":0}
        false_inf = {"P": 0, "N":0}
        for index, line in enumerate(f_in):
            if index == 0:
                continue
            line_inf = line.strip().split("\t")
            true_label = line_inf[0]
            predict_label = line_inf[-2]
            if true_label == label_str:
                if predict_label == label_str:
                    true_inf["P"] = true_inf["P"] + 1
                else:
                    true_inf["N"] = true_inf["N"] + 1
            else:
                if predict_label == label_str:
                    false_inf["P"] = false_inf["P"] + 1
                else:
                    false_inf["N"] = false_inf["N"] + 1
        print "label: ", label_str
        print "true_positive: %s, true_negative: %s\n" \
                % (str(true_inf["P"]), str(true_inf["N"]))
        print "false_positive: %s, false_negative: %s\n" \
                % (str(false_inf["P"]), str(false_inf["N"]))
        precise_true = true_inf["P"]/float(true_inf["P"] + false_inf["P"])
        recall_true = true_inf["P"]/float(true_inf["P"] + true_inf["N"])
        print str(precise_true), str(recall_true)
        precise_false = false_inf["N"]/float(false_inf["N"] + true_inf["N"])
        recall_false = false_inf["N"]/float(false_inf["N"] + false_inf["P"])
    with codecs.open(sys.argv[2]+label_str, "w", "utf-8") as f_out:
        f_out.write("true_positive: %s, true_negative: %s\n" \
                % (str(true_inf["P"]), str(true_inf["N"])))
        f_out.write("false_positive: %s, false_negative: %s\n" \
                % (str(false_inf["P"]), str(false_inf["N"])))
        f_out.write("positive_precise: %s, positive_recall: %s\n" \
                % (str(precise_true), str(recall_true)))




