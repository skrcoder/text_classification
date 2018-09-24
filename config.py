# coding=utf-8
# Author: zhengxiongfeng
# mail: 657019943@qq.com
# github: https://github.com/skrcoder
#!/usr/bin/python

train_data_path = "data/cnews.train.txt"
test_data_path = "data/cnews.test.txt"
val_data_path = "data/cnews.val.txt"

# 1. lr
#model_type = "logistic_regression" # 可选model参数见下面的get_model（）部分
#model_data_path = "../models_files/lr/lr.pkl"
#model_pr_data_path = "../models_files/lr/lr_pr_time.txt"

# 2. svm
model_type = "svm" # 可选model参数见下面的get_model（）部分
model_data_path = "../models_files/svm/svm.pkl"
model_pr_data_path = "../models_files/svm/svm_pr_time.txt"

# 3. decision_tree
model_type = "decision_tree" # 可选model参数见下面的get_model（）部分
model_data_path = "../models_files/decision_tree/decision_tree.pkl"
model_pr_data_path = "../models_files/decision_tree/decision_tree_pr_time.txt"

# 4. adaboost
model_type = "random_forest" # 可选model参数见下面的get_model（）部分
model_data_path = "../models_files/random_forest/random_forest.pkl"
model_pr_data_path = "../models_files/random_forest/random_forest_pr_time.txt"

# 5. gbdt
model_type = "gbdt" # 可选model参数见下面的get_model（）部分
model_data_path = "../models_files/gbdt/gbdt.pkl"
model_pr_data_path = "../models_files/gbdt/gbdt_pr_time.txt"

# 6. xgboost
model_type = "xgboost" # 可选model参数见下面的get_model（）部分
model_data_path = "../models_files/xgboost/xgboost.pkl"
model_pr_data_path = "../models_files/xgboost/xgboost_pr_time.txt"

# 7. bagging
model_type = "bagging" # 可选model参数见下面的get_model（）部分
model_data_path = "../models_files/bagging/bagging.pkl"
model_pr_data_path = "../models_files/bagging/bagging_pr_time.txt"

# 8. stacking
model_type = "stacking" # 可选model参数见下面的get_model（）部分
model_data_path = "../models_files/stacking/stacking.pkl"
model_pr_data_path = "../models_files/stacking/stacking_pr_time.txt"




