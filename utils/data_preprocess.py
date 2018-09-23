# coding=utf-8
# Author: zhengxiongfeng
# mail: 657019943@qq.com
# github: https://github.com/skrcoder
#!/usr/bin/python

import os
import codecs
import jieba
import jieba.posseg

def get_custom_stopwords(stopwords_file_data):
    stopwords_list = []
    with codecs.open(stopwords_file_data, "r", "utf-8") as f_in:
        stopwords_list = [tmp.strip("\n") for tmp in f_in.readlines()]
    return stopwords_list

def seg_data(in_file, out_file, re_run=False, possseg=False):
    if os.path.exists(out_file) and not re_run:
        print "seg data already exist!"
        return None
    with codecs.open(in_file, "r", "utf-8") as f_in, \
            codecs.open(out_file, "w", "utf-8") as f_out:
         for index, line in enumerate(f_in):
             fields = line.strip("\n").split("\t")
             if len(fields) != 2:
	             print "the %d line of input data form err!" % (index)
	             continue
             label = fields[0]
             content = "".join(fields[1:]).replace(" ", "").replace("\n", "")
             seg_line = None
             if possseg:
                 words = jieba.posseg.cut(content)
                 tmp_list = []
                 for word, pos in words:
                     tmp_list.append(word + "/" + pos)
                 seg_line = " ".join(tmp_list)
             else:
                 words = jieba.cut(content)
                 seg_line = " ".join(words)
             f_out.write("\t".join([label, seg_line]) + "\n")

if __name__ == "__main__":
    train_data_path = "../data/cnews/cnews.train.txt"
    train_data_seg_path = "../data/cnews/cnews.train.seg.txt"
    test_data_path = "../data/cnews/cnews.test.txt"
    test_data_seg_path = "../data/cnews/cnews.test.seg.txt"
    val_data_path = "../data/cnews/cnews.val.txt"
    val_data_seg_path = "../data/cnews/cnews.val.seg.txt"

    #seg_data(test_data_path, test_data_seg_path)
    #seg_data(train_data_path, train_data_seg_path)
    seg_data(val_data_path, val_data_seg_path)
