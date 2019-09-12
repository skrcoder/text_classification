#!/usr/bin/env python
#-*- coding: gb18030 -*-
################################################################################
#
# Copyright (c) 2016 Baidu.com, Inc. All Rights Reserved
#
################################################################################
"""
This module provide mapper function of kuadayongyu recognization.
Authors: chenmingquan01(chenmingquan01@baidu.com)
Date:    2016/11/08 20:04:00
"""

import sys
reload(sys)
sys.setdefaultencoding('gb18030')
import os
sys.path.append('wordseg/lib')
sys.path.append('wordseg/conf')

import conf
import wordseg
import util
import re
import postag
import math
import traceback

class WordSeggerUtil(object):
    """分词器
    """

    def __init__(self):
        """类初始化
        """
        path_prefix = "wordseg/"
        util.WordSegger.init_conf( \
                path_prefix + conf.SEGDICT_PATH, \
                path_prefix + conf.TAGDICT_PATH, \
                path_prefix + conf.STOPWORD_PATH)
        self.word_segger = util.WordSegger.get_segger()
        #self.stopword_dict = self.load_stopword_dict('conf/dict/stop_word.txt')

    def load_stopword_dict(self, stopword_file):
        """加载停用词典
        """
        stopword_dict = {}
        with open(stopword_file, 'r') as fd:
            for line in fd:
                fields = line.strip('\n').split('\t')
                word = fields[0].decode('gb18030', 'ignore')
                stopword_dict[word] = None

        return stopword_dict

    def wordseg_execute(self, line):
        """混排粒度分词器调用
        """
        word_list = self.word_segger.get_tokens(line)
        return word_list

    def wordseg_execute_normal(self, line):
        """基本粒度分词器调用
        """
        word_list = self.word_segger.get_tokens_normal(line)
        return word_list

    def postag_execute(self, line):
        """混排粒度切词的词性标注
        """
        label_word_list = self.word_segger.get_word_tags(line)
        return label_word_list

    def postag_execute_normal(self, line):
        """基本粒度切词的词性标注
        """
        label_word_list = self.word_segger.get_word_tags_normal(line)
        return label_word_list

    def split_word_and_label(self, label_word_list):
        """分离词与标签

        分离词与词性标签，同时去除空格与符号/
        """
        label_list = []
        word_list = []
        for word_tag_pair in label_word_list:
            word = word_tag_pair[0]
            label = word_tag_pair[1]
            # 去掉空格
            if len(word.strip()) == 0:
                continue
            # 去掉斜杠/
            if word == '/':
                continue

            try:
                word = word.decode('gb18030', 'ignore')
                #if len(word) < 2:
                #    continue
                #if word in self.stopword_dict:
                #    continue

                if label == 'ns':
                    continue
            except UnicodeDecodeError as e:
                continue
            word_list.append(word)
            label_list.append(label)
        return word_list, label_list

    def word_seg_util_run(self, record, model=0):
        """句子的词性标注调用主函数

        提供基本粒度与混排粒度的词性标注.

        Args:
            record: a string, 待词性标注的句子.
            model: a int, 基本粒度与混排粒度切词的选择标识
                   值为0 选择基本粒度
                   值不为0 选择混排粒度

        Returns:
            seg_result: a string, 带词性标注的结果
                        词间隔通过标识空格' '来区分
        """
        try:
            if model == 0:
                label_word_list = self.postag_execute_normal(record)
            else:
                label_word_list = self.postag_execute(record)
            word_list, label_list = self.split_word_and_label(label_word_list)
            word_tag_list = zip(word_list, label_list)
            word_seg_list = []
            if len(word_list) == 0:
                return None
            for word_tag in word_tag_list:
                labeled_word = '/'.join(list(word_tag))
                word_seg_list.append(labeled_word)
            seg_result = ' '.join(word_seg_list).encode("gb18030")
            return seg_result
        except Exception as e:
            return None

    def postag_util_run(self, record, mode=0):
        """句子的词性标注调用主函数

        提供基本粒度与混排粒度的词性标注.

        Args:
            record: a string, 待词性标注的句子.
            mode: a int, 基本粒度与混排粒度切词的选择标识
                   值为0 选择基本粒度
                   值不为0 选择混排粒度

        Returns:
            word_label_list: a list, [(word, label),...]
        """
        try:
            if mode == 0:
                label_word_list = self.postag_execute_normal(record)
            else:
                label_word_list = self.postag_execute(record)
            word_list, label_list = self.split_word_and_label(label_word_list)
            word_label_list = zip(word_list, label_list)
            if len(word_list) == 0:
                return None
            return word_label_list
        except Exception as e:
            return None


if __name__ == '__main__':
    word_segger_util = WordSeggerUtil()
    word_label_list = word_segger_util.postag_util_run("江门民康男科门诊部", mode=1)
    word_list, label_list = zip(*word_label_list)
    print '\t'.join(word_list)
    print '\t'.join(label_list)
# vim: tw=100 ts=4 sw=4 cc=100
