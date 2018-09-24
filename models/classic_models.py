# coding=utf-8
# Author: zhengxiongfeng
# mail: 657019943@qq.com
# github: https://github.com/skrcoder
#!/usr/bin/python

import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import codecs
import pickle

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.neural_network import MLPClassifier

from xgboost import XGBClassifier

from mlxtend.classifier import EnsembleVoteClassifier, StackingClassifier

from sklearn.metrics import classification_report
from sklearn.model_selection import cross_validate

sys.path.append("../utils/")
from data_preprocess import get_custom_stopwords
import config

# 1. 配置config中的model_type 和model_data_path和model_pr_data_path
# model_type = "logistic_regression" # 可选model参数见下面的get_model（）部分
# model_data_path = "../models_files/lr/lr.pkl"
# model_pr_data_path = "../models_files/lr/lr_pr_time.txt"
model_type = config.model_type
model_data_path = config.model_data_path
model_pr_data_path = config.model_pr_data_path

def save_model(model_save_path, classifier):
    file_dir = model_save_path.rsplit("/", 1)[0]
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    with open(model_data_path, "wb") as f_in:
        pickle.dump(classifier, f_in)

def load_model(model_save_path):
    with open(model_data_path, "rb") as f_in:
        clf = pickle.load(f_in)
    return clf

def save_model_pr(model_pr_data_path, model_pr):
    file_dir = model_pr_data_path.rsplit("/", 1)[0]
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    with open(model_pr_data_path, "wb") as f_in:
        for key, value in model_pr.items():
            tmp_list = [str(tmp) for tmp in value]
            f_in.write(key + ":\t" + " ".join(tmp_list) + "\n")

def get_model(model_type):
    if model_type == "knn":
        model = KNeighborsClassifier()
    elif model_type == "naive_bayes":
        model = MultinomialNB()
    elif model_type == "logistic_regression":
        model = LogisticRegression()
    elif model_type == "svm":
        model = SVC(kernel='linear')
    elif model_type == "decision_tree":
        model = DecisionTreeClassifier()
    elif model_type == "adaboost":
        model = AdaBoostClassifier()
    elif model_type == "random_forest":
        model = RandomForestClassifier(n_estimators=300)
    elif model_type == "gbdt":
        model = GradientBoostingClassifier()
    elif model_type == "xgboost":
        model = XGBClassifier()
    elif model_type == "mlp":
        model = MLPClassifier()
    elif model_type == 'bagging':
        clf1 = LogisticRegression(random_state=0)
        clf2 = XGBClassifier(random_state=0)
        clf3 = SVC(random_state=0, kernel='linear', probability=True)
        clf4 = MLPClassifier(random_state=0)
        model = EnsembleVoteClassifier(clfs=[clf1, clf2, clf3, clf4],
                                       weights=[1, 2, 2, 1], voting='soft', verbose=2)
    elif model_type == 'stacking':
        clf1 = XGBClassifier(random_state=0)
        clf2 = SVC(random_state=0, kernel='linear', probability=True)
        clf3 = MLPClassifier(random_state=0)
        lr = LogisticRegression()
        model = StackingClassifier(classifiers=[clf1, clf2, clf3],
                                  use_probas=True,
                                  average_probas=False,
                                  meta_classifier=lr)
    return model


if __name__ == "__main__":
    # load train data and test data
    #train_data_path = "../data/cnews/cnews.train.seg.txt"
    test_data_path = "../data/cnews/cnews.test.seg.txt"
    #val_data_path = "../data/cnews/cnews.val.seg.txt"

    #train_data = pd.read_table(train_data_path, header=None)
    test_data = pd.read_table(test_data_path, header=None)
    #val_data = pd.read_table(val_data_path, header=None)
    print "load seg data done"

    # load stopwords
    stopword_data_path = "../data/stopwords.txt"
    stopwords_list = get_custom_stopwords(stopword_data_path)
    print "load stopwords done"

    # labels_desc, featrue_desc
    #labels_desc, feature_desc = train_data[0], train_data[1]
    # use less data
    labels_desc, feature_desc = test_data[0], test_data[1]

    # labels encoder
    enc = LabelEncoder()
    enc.fit(labels_desc)
    train_labels = enc.transform(labels_desc)
    #test_labels = enc.transform(test_data[0])
    #val_labels = enc.transform(val_data[0])
    print "label encode done"

    # feature encoder
    vecorizer = CountVectorizer(max_df=0.8, min_df=3, stop_words=frozenset(stopwords_list))
    train_features = vecorizer.fit_transform(feature_desc)
    #feature_names = vecorizer.get_feature_names()
    #test_features = vecorizer.transform(test_data[1])
    #val_features = vecorizer.transform(val_data[1])
    print "feature encode done"

    # get model
    classifier = get_model(model_type)
    #classifier.fit(train_features, train_labels)
    print "get model done"

    # test
    #print classifier.score(test_features, test_labels) # 0.9581
    #print classifier.score(val_features, val_labels) #0.9336
    #labels_inf = list(enc.classes_)
    #test_predict = classifier.predict(test_features)
    #val_predict = classifier.predict(val_features)
    #print classification_report(test_labels, test_predict, target_names=labels_inf)
    #print classification_report(val_labels, val_predict, target_names=labels_inf)

    # cross validation and eval
    # TODO: 自定义socre
    cv_result = cross_validate(classifier, train_features, train_labels, cv=3, \
                               return_train_score=False, n_jobs=-1)
    save_model_pr(model_pr_data_path, cv_result)
    print "cross validation done"

    # save and load model
    save_model(model_data_path, classifier)
    clf = load_model(model_data_path)
    #print clf.score(test_features, test_labels)
    print "save and load model done"

