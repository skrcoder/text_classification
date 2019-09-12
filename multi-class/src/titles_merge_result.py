#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: titles_merge_result.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2017/08/01 21:17:18
"""
import sys
import codecs

"""
python titles_merge_result.py sys.agrv[1] sys.argv[2] sys.argv[3]
sys.agrv[1]:LR模型的预测结果,(1):1\n-1\n1...,(2):label 1 -1\n 1 p_1 p_-1\n-1 p_1 p_-1
sys.argv[2]:原始数据:label\tcontent
sys.argv[3]:输出数据:label\tLR_result\tprobability
sys.argv[4]:特征文件:index\t特征名\t卡方值\t特征权重
sys.argv[5]:分词后的文件:label\t分词结果（空格分开）
"""

with codecs.open(sys.argv[4], "r", "utf-8") as f_feature_dict, \
        codecs.open(sys.argv[5], "r", "utf-8") as f_wordseg_result:
    feature_inf_dict = dict()
    wordseg_result_list = []
    for line in f_feature_dict:
        line_inf = line.strip().split("\t")
        feature_name = line_inf[1]
        feature_inf = "||".join(line_inf[2:])
        feature_inf_dict[feature_name] = feature_inf
    wordseg_result_list = [tmp.strip().split("\t")[1].split(" ") \
            for tmp in f_wordseg_result.readlines()]

def get_evidence(sample_index):
    """
    得到命中的特征结果
    """
    wrodseg_result = wordseg_result_list[sample_index]
    evidence = []
    for item in wrodseg_result:
        if item in feature_inf_dict:
            #evidence.append("||".join(["word_"+item, feature_inf_dict[item]]))
            evidence.append(item)
    return "||".join(evidence)

with codecs.open(sys.argv[1], "r", "utf-8") as f_dict:
    line_inf_list = []
    for index, line in enumerate(f_dict):
        if index == 0:
            labels_list = line.strip().split()
        else:
            line_inf_list.append(line.strip().split())

with codecs.open(sys.argv[2], "r", "utf-8") as f_in, \
        codecs.open(sys.argv[3], "w", "utf-8") as f_out:
    result = list()
    #存在相同的样本
    threshold = 0.7
    #threshold = 0.65
    print "threshold: ", threshold
    for index, line in enumerate(f_in):
        msg = line.strip().split("\t")
        if len(msg) < 2:
            print "sample length err:", index
            continue
        predict_label_str = line_inf_list[index][0]
        labels_inf = labels_list[1:]
        predict_confident_inf = line_inf_list[index][1:]
        labels_confident_dict = dict(zip(labels_inf, predict_confident_inf))
        labels_confident = labels_confident_dict[predict_label_str]
        #soted_labels_confident = sorted(labels_confident_dict.items(), key=lambda x:-float(x[1]))
        soted_labels_confident = zip(labels_inf, predict_confident_inf)
        all_labels_confident_str = " ".join([tmp[0] + ":" + tmp[1] \
                for tmp in soted_labels_confident])
        evidence_str = get_evidence(index)
        #out_inf = "\t".join([msg[0], msg[1].replace("\t", "").replace(" ", ""), predict_label_str, labels_confident, all_labels_confident_str, evidence_str])
        out_inf = "\t".join([msg[0], msg[1].replace("\t", "").replace(" ", ""), \
                predict_label_str, labels_confident, evidence_str])
        result.append(out_inf)
    print "merge sample result length:", index
    #print "not unique and sorted merge sample result length:", len(result)
    f_out.write("\t".join(labels_list) + "\n")
    for item in result:
        f_out.write(item + "\n") 
    print "merge train result done"
    

