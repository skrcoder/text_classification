# coding=utf-8
# Author: zhengxiongfeng
# mail: 657019943@qq.com
# github: https://github.com/skrcoder
#!/usr/bin/python


import config
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
sys.path.append("../utils/")
from data_preprocess import get_custom_stopwords

if __name__ == "__main__":
    # load train data and test data
    train_data_path = "../data/cnews/cnews.train.seg.txt"
    test_data_path = "../data/cnews/cnews.test.seg.txt"
    val_data_path = "../data/cnews/cnews.val.seg.txt"

    train_data = pd.read_table(train_data_path, header=None)
    test_data = pd.read_table(test_data_path, header=None)
    val_data = pd.read_table(val_data_path, header=None)

    # load stopwords
    stopword_data_path = "../data/stopwords.txt"
    stopwords_list = get_custom_stopwords(stopword_data_path)

    # labels_desc, featrue_desc
    labels_desc, feature_desc = train_data[0], train_data[1]

    # labels encoder
    enc = LabelEncoder()
    enc.fit(labels_desc)
    labels = enc.transform(labels_desc)
    test_labels = enc.transform(test_data[0])
    val_labels = enc.transform(val_data[0])

    # feature encoder
    vecorizer = CountVectorizer(max_df=0.8, min_df=3, stop_words=frozenset(stopwords_list))
    features = vecorizer.fit_transform(feature_desc)
    feature_names = vecorizer.get_feature_names()
    test_features = vecorizer.transform(test_data[1])
    val_features = vecorizer.transform(val_data[1])

    # lr model
    lr_classifier = LogisticRegression()
    lr_classifier.fit(features, labels)

    # test
    labels_inf = list(enc.classes_)
    test_predict = lr_classifier.predict(test_features)
    val_predict = lr_classifier.predict(val_features)
    print classification_report(test_labels, test_predict, target_names=labels_inf)
    print classification_report(val_labels, val_predict, target_names=labels_inf)

    #print lr_classifier.score(test_features, test_labels) # 0.9581
    #print lr_classifier.score(val_features, val_labels) #0.9336



