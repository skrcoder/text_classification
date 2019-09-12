#!/bin/sh


#tips:需要修改的参数作为变量定义
#待处理的数据目录路径
#基目录下包含文件：[baimingdan],train/, test/, 生成文件：feature, lr_model, lr_model.out
#base_data_path="/home/users/zhengxiongfeng/cloud-disk/lr/data/politics/"
base_data_path="/home/users/zhengxiongfeng/cloud-disk/lr/data/porn/"
train_data_path=${base_data_path}"train/"
test_data_path=${base_data_path}"test/"
#test_data1:feed
#test_data_path=${base_data_path}"feed/"
#test_data2:feed2
#test_data_path=${base_data_path}"feed2/"
#test_data3:wenda
#test_data_path=${base_data_path}"wenda/"
#liblinear得到的模型文件
model_file=${base_data_path}"lr_model.long.topic"
#最终得到的模型文件
model_file_path=${base_data_path}"lr_model.long.topic.out"
#生成的主题特征文件
topic_feature_file_name=".topic_feature"
topic_feature_num=5

if [ $1 == "train" ]
then
    python feature_add.py ${train_data_path}${2}${topic_feature_file_name} ${topic_feature_num} ${base_data_path}"feature" ${base_data_path}"feature.new"
    python gen_instance.topic.py ${train_data_path}${2}".wordseg" ${train_data_path}${2}".wordseg.instance.topic" ${train_data_path}${2}${topic_feature_file_name} ${topic_feature_num} ${base_data_path}"feature.new"
    ./lr_train -s 0 ${train_data_path}${2}".wordseg.instance.topic" ${model_file}
    python lr_merge_feature.topic.py ${model_file} ${base_data_path}"feature.new" ${model_file_path} 
elif [ $1 == "test" ]
then
    python gen_instance.topic.py ${test_data_path}${2}".wordseg" ${test_data_path}${2}".wordseg.instance.topic" ${test_data_path}${2}${topic_feature_file_name} ${topic_feature_num} ${base_data_path}"feature.new"
    ./lr_predict -b 1 ${test_data_path}${2}".wordseg.instance.topic" ${model_file} ${test_data_path}${2}".wordseg.instance.result"
    python titles_merge_result.py ${test_data_path}${2}".wordseg.instance.result" ${test_data_path}${2}".wordseg.ok"  ${test_data_path}${2}".wordseg.instance.result.merge.topic"
    python static.py ${test_data_path}${2}".wordseg.instance.result.merge.topic" ${test_data_path}${2}".wordseg.instance.result.merge.static.topic"

fi
