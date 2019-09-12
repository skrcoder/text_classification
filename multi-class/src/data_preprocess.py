#!/usr/bin/env python
# -*- coding: utf-8 -*-
########################################################################
# 
# Copyright (c) 2017 Baidu.com, Inc. All Rights Reserved
# 
########################################################################
 
"""
File: sample_wordseg.py
Author: zhengxiongfeng(zhengxiongfeng@baidu.com)
Date: 2017/08/01 16:39:02
"""
import os
import sys
import codecs
import re

from wordseg_run_hadoop import WordSeggerUtil

class DataPreprocess(object):
    """
    数据预处理：
    step1. 去掉无意义符号。
    step2. 分词。
    step3. 去掉停用词（包含标点符号）。
    step4. 得到n-gram特征。
    """
    def __init__(self, wordsegger_util, n_gram, stopword_file):
        self.word_segger_util = wordsegger_util
        self.n_gram = n_gram
        self.stopword_set = self.load_stopword_set(stopword_file)

        # 无意义符号
        self.region_invest_str = u"{地域}{投放地域}"
        self.pair_str = u"{关键词}"
        
        # 纯数字和字母pattern
        self.word_digital_pattern = re.compile(r"^[0-9]+$")
        self.word_char_pattern = re.compile(r"^[a-zA-Z]$")

    def load_stopword_set(self, stopword_file):
        """
        加载停用词表
        """
        stopword_set = set()
        with codecs.open(stopword_file, "r", "gb18030") as fd:
            for line in fd:
                content = line.strip("\n")
                stopword_set.add(content)
        return stopword_set

    def filter_unvalid_word(self, token_list):
        """
        去掉无意义符号
        """
        new_token_list = []
        for token in token_list:
            digital_match = self.word_digital_pattern.match(token)
            char_match = self.word_char_pattern.match(token)
            if (not digital_match) and (not char_match):
                new_token_list.append(token)
        return new_token_list

    def get_ngram(self, word_list, max_order, max_order_only=False):
        """
        生成n-gram特征
        """
        start_order = self.max_order if max_order_only else 1
        ngram_list = []
        for order_index in range(start_order, max_order + 1):
            for seq_index in range(0, len(word_list) - order_index + 1):
                sub_tokens = word_list[seq_index: seq_index + order_index]
                ngram = "_".join([tmp for tmp in sub_tokens if tmp])
                ngram_list.append(ngram)
        return ngram_list

    def run(self, input_file_path):
        """
        核心执行函数
        """
        with codecs.open(input_file_path, "r", "utf-8") as f_in,\
                codecs.open(input_file_path + ".wordseg", "w", "utf-8") as f_out,\
                codecs.open(input_file_path + ".wordseg.ok", "w", "utf-8") as f_ok,\
                codecs.open(input_file_path + ".wordseg.err", "w", "utf-8") as f_err:
            for index, line in enumerate(f_in):
                fields = line.strip().split("\t")
                if len(fields) < 3:
                    print "title length err:" + str(index)
                    f_err.write(line)
                    continue
                label = fields[0]
                msg_type = fields[1]
                msg = fields[2]
                # step1. 去掉无意义符号。
                msg = msg.replace(self.region_invest_str, "")
                msg = msg.replace(self.pair_str, "").replace(u"{", "").replace(u"}", "")
                msg_gbk = msg.encode("gb18030")
                try:
                    # step2. 分词。
                    word_pos_list = self.word_segger_util.postag_util_run(msg_gbk, mode=1)
                except UnicodeEncodeError as e:
                    print "err:", e.message
                    f_err.write(line)
                    continue
                # step3. 去掉停用词（包含标点符号）。
                word_list, pos_list = zip(*word_pos_list)
                word_list = self.filter_unvalid_word(word_list) 
                if not word_list:
                    f_err.write(line)
                    continue
                # step4. 得到n-gram特征。
                ngram_list = self.get_ngram(word_list, self.n_gram)
                
                if msg_type == "keyword":
                    token_list = ["keyword_" + tmp for tmp in ngram_list]
                else:
                    token_list = ["idea_" + tmp for tmp in ngram_list]

                if len(token_list) > 0:
                    f_out.write(label + "\t" + " ".join(token_list) + "\n")
                    f_ok.write(line)
                else:
                    f_err.write(line)
                    print "wordseg err:" + str(index)


def main():
    """
    主函数
    """
    input_file = sys.argv[1]
    stopword_file = sys.argv[2]
    n_gram = int(sys.argv[3])
    wordsegger_util = WordSeggerUtil()
    data_preprocesser = DataPreprocess(wordsegger_util, n_gram, stopword_file)
    data_preprocesser.run(input_file)

if __name__ == "__main__":
    main()
