#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: sklearn.feature.selection.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2017/08/10 11:53:18
"""
import sys
import os
import codecs
import pprint

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectPercentile
from sklearn.feature_selection import SelectKBest

class FeatureSelection(object):
    """
    特征选择类
    """
    def __init__(self, feature_keep_precent, feature_keep_num, feature_min_df):
        self.feature_keep_precent = int(feature_keep_precent)
        self.feature_keep_num = int(feature_keep_num)
        self.feature_min_df = int(feature_min_df)
        self.ch2_precent = SelectPercentile(chi2, percentile=self.feature_keep_precent)
        self.ch2_num = SelectKBest(chi2, k=self.feature_keep_num)

    def run(self, input_file_path, feature_output_file, is_precent=True):
        """
        核心执行函数
        """
        with codecs.open(input_file_path, "r", "utf-8") as f_in:
            tmp_list = f_in.readlines()
            x_train = [tmp.strip().split("\t")[1] for tmp in tmp_list]
            y_train = [tmp.strip().split("\t")[0] for tmp in tmp_list]
            vectorizer = CountVectorizer(min_df=self.feature_min_df)
            x_train = vectorizer.fit_transform(x_train)
            print "feature set num: ", len(vectorizer.vocabulary_)
            feature_names = vectorizer.get_feature_names()
            if is_precent:
                ch2 = self.ch2_precent.fit(x_train, y_train)
            else:
                ch2 = self.ch2_num.fit(x_train, y_train)
            scores, pval = ch2.scores_, ch2.pvalues_
            x_train = ch2.transform(x_train)
            features = [feature_names[i] for i in ch2.get_support(indices=True)]
            feature_scores = [scores[i] for i in ch2.get_support(indices=True)]
            sorted_feature = sorted(zip(features, feature_scores), key=lambda x:x[1], reverse=True)
        
            with codecs.open(feature_output_file, "w", "utf-8") as f_out:
                for id, item in enumerate(sorted_feature):
                    f_out.write("\t".join([str(id + 1), item[0], str(item[1])]) + "\n")
        
            print "feature select done,new feature set num: ", len(feature_scores)


def main():
    """
    主函数
    """
    is_precent = True if sys.argv[1] == "1" else False
    feature_keep_precent = sys.argv[2]
    feature_keep_num = sys.argv[3]
    feature_min_df = sys.argv[4]
    input_file_path = sys.argv[5]
    feature_output_file = sys.argv[6]
    feature_selection = FeatureSelection(feature_keep_precent, feature_keep_num, feature_min_df) 
    feature_selection.run(input_file_path, feature_output_file, is_precent)

if __name__ == "__main__":
    main()
