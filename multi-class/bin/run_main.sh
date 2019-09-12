#!/bin/sh

source bin/shell_utils.sh
source conf/conf.sh

LOG_PATH="log"
LOG_FILE="run_main.log"

DATE=`date -d "-1 days" +%Y%m%d`

### 清空日志目录
rm -rf log/*
WriteLog $? "clean_log_sh"

# 训练数据文件
train_data_file="./data/train/"${TRAIN_DATA_FILE_NAME}

# 测试数据文件
test_data_file="./data/test/"${TEST_DATA_FILE_NAME}

# 特征选择的输出文件
feature_file="./data/feature/feature"

# liblinear得到的模型文件
model_file_path="./data/model/lr_model_mutilclass"

if [ $1 == "train" ]
then
    ${PYTHON_HOME}/bin/python src/data_preprocess.py ${train_data_file} ${STOPWORD_FILE_PATH} ${N_GRAM_NUM}
    WriteLog $? "data_preprocess_sh"

    ${PYTHON_HOME}/bin/python src/feature_selection.py ${IS_PRECENT} ${FEATURE_KEEP_PRECENT} ${FEATURE_KEEP_NUM} ${FEATURE_MIN_DF} ${train_data_file}".wordseg" ${feature_file} 
    WriteLog $? "feature_selection_sh"
    
    ${PYTHON_HOME}/bin/python src/gen_instance.py ${feature_file} ${train_data_file}".wordseg" ${train_data_file}".wordseg.instance"
    WriteLog $? "gen_instance_sh"

    ${LIBLINEAR_TRAIN} -s 0 ${train_data_file}".wordseg.instance" ${model_file_path}
    WriteLog $? "lr_train_sh"

    ${PYTHON_HOME}/bin/python src/lr_merge_feature.py ${model_file_path} ${feature_file} ${model_file_path}".desc"
    WriteLog $? "merge_model_desc_sh"

elif [ $1 == "test" ]
then
    ${PYTHON_HOME}/bin/python src/data_preprocess.py ${test_data_file} ${STOPWORD_FILE_PATH} ${N_GRAM_NUM} 
    WriteLog $? "data_preprocess_sh"
    
    ${PYTHON_HOME}/bin/python src/gen_instance.py ${feature_file} ${test_data_file}".wordseg" ${test_data_file}".wordseg.instance"
    WriteLog $? "gen_instance_sh"

    ${LIBLINEAR_PREDICT} -b 1 ${test_data_file}".wordseg.instance" ${model_file_path} ${test_data_file}".wordseg.instance.result"
    WriteLog $? "lr_predict_sh"

    ${PYTHON_HOME}/bin/python src/titles_merge_result.py ${test_data_file}".wordseg.instance.result" ${test_data_file}".wordseg.ok" ${test_data_file}".wordseg.instance.result.merge" ${model_file_path}".desc.all" ${test_data_file}${2}".wordseg" 
    WriteLog $? "merge_predict_result_sh"

    ${PYTHON_HOME}/bin/python src/static_multi_class.py ${test_data_file}".wordseg.instance.result.merge" ${test_data_file}".wordseg.instance.result.merge.static"
    WriteLog $? "static_precision_recall_sh"

    #python static.py ${test_data_path}${2}".wordseg.instance.result.merge" ${test_data_path}${2}".wordseg.instance.result.merge.static"
    #python static_multi_class.py  ${test_data_path}${2}".wordseg.instance.result.merge" ${test_data_path}${2}".wordseg.instance.result.merge.static"
fi

WriteLog $? "run_main_sh"
