### 配置文件
# hadoop 路径
HADOOP_HOME="/home/users/zhengxiongfeng/hadoop-client/hadoop-client-mulan/hadoop"

# Python 环境
PYTHON_HOME="/home/users/zhengxiongfeng/cloud-disk/python27-gcc482"

# liblinear 路径
LIBLINEAR_TRAIN="./liblinear-2.11/train"
LIBLINEAR_PREDICT="./liblinear-2.11/predict"

# 训练数据文件名:需要放在./data/train/目录下
TRAIN_DATA_FILE_NAME="input"

# 测试数据文件名：需要放在./data/test/目录下
TEST_DATA_FILE_NAME="input"

# 停用词文件路径
STOPWORD_FILE_PATH="data/dict/stopword.txt"

# n-gram特征
N_GRAM_NUM=2

# 选择特征保留方法(默认使用百分比的方式)
IS_PRECENT=1

# 特征选择时保留特征百分比,70表示保留70%数量的特征
FEATURE_KEEP_PRECENT=70

# 特征选择时保留特征数量
FEATURE_KEEP_NUM=10

# 特征选择时最小出现频次
FEATURE_MIN_DF=3

