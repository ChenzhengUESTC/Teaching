# encoding=utf-8
import pickle

import jieba
import json
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

train_file = "train.json"
test_file = "test.json"
model_file = "naive_bayes_model.m"
stopwords_file = 'stopwords_cn.txt'

feature_size = 1000


def load_data(file_name):
    with open(file_name, 'r') as file_name:
        data = json.load(file_name)
        for sample in data:
            sample["seged_content"] = list()
            seged_content = jieba.cut(sample["content"])
            for word in seged_content:
                sample["seged_content"].append(word)
    return data


def load_word_list(train_data):
    # 统计词频放入all_words_dict
    all_word_list = list()
    all_words_dict = {}
    for train_sample in train_data:
        word_list = train_sample["seged_content"]
        for word in word_list:
            if word in all_words_dict:
                all_words_dict[word] += 1
            else:
                all_words_dict[word] = 1
    # key函数利用词频进行降序排序
    all_words_tuple_list = sorted(all_words_dict.items(), key=lambda f: f[1], reverse=True)  # 内建函数sorted参数需为list
    all_words_list = list(list(zip(*all_words_tuple_list))[0])
    return all_words_list


def load_stopword(stopwords_file):
    # 生成stopwords_set
    stopwords_set = set()
    with open(stopwords_file, 'r') as fp:
        for line in fp.readlines():
            word = line.strip()
            if len(word) > 0 and word not in stopwords_set:  # 去重
                stopwords_set.add(word)
    return stopwords_set


def get_feature_words(all_words_list, stopwords_set):
    ## 文本特征提取和分类
    feature_words = []
    for t in range(0, len(all_words_list), 1):
        if len(feature_words) > feature_size:  # feature_size是feature_words的维度1000
            break
        if not all_words_list[t].isdigit() and all_words_list[t] not in stopwords_set and 1 < len(
                all_words_list[t]) < 5:
            feature_words.append(all_words_list[t])
    return feature_words


def prepair_data(data, feature_words):
    for sample in data:
        word_list = sample["seged_content"]
        features = [1 if word in word_list else 0 for word in feature_words]
        sample["features"] = features
    feature_list = list()
    class_list = list()
    for sample in data:
        feature_list.append(sample["features"])
        class_list.append(sample["label"])
    return feature_list, class_list


def save_mode(model_file, classifier, feature_words):
    with open(model_file, "wb") as model_file:
        pickle.dump(classifier, model_file)
        pickle.dump(feature_words, model_file)
        model_file.close()


if __name__ == '__main__':
    # 加载数据
    train_data = load_data(train_file)
    test_data = load_data(test_file)

    # 统计数据中的所有的词，构成词表
    # 思考：为什么只统计train_data，不统计test_data
    all_words_list = load_word_list(train_data)
    print("词表统计完成, len(all_words_list)=", len(all_words_list))

    # 加载"停用词"表，既是一些预先定义好的，对文本分类无意义的常见词
    stopwords_set = load_stopword(stopwords_file)
    print("停用词表加载完成, len(stopwords_set)=", len(stopwords_set))

    # 用词表中的高频词，去除掉停用词，构成特征词表
    feature_words = get_feature_words(all_words_list, stopwords_set)
    print("特征词表提取完成, feature_words: ", feature_words)

    # 按照sklearn的要求准备数据
    train_feature_list, train_class_list = prepair_data(train_data, feature_words)
    test_feature_list, test_class_list = prepair_data(test_data, feature_words)
    # 调用sklearn的MultinomialNB，训练朴素贝叶斯模型
    classifier = MultinomialNB().fit(train_feature_list, train_class_list)
    # 你自己实现一个Your_Naive_Bayes，用来替换MultinomialNB。
    # Your_Naive_Bayes里面需要实现两个方法：fit()和predict()，分别实现朴素贝叶斯模型的训练和预测
    # classifier=Your_Naive_Bayes().fit(train_feature_list, train_class_list)

    # 用训练好的模型对测试数据进行分类
    test_class_pred = classifier.predict(test_feature_list)

    # 统计分类结果，计算Precision Recall 和 F1-score
    target_names = ["文化", "娱乐", "体育", "财经", "房产", "汽车", "教育", "科技", "军事", "旅游", "国际", "证券", "农村", "游戏", "社会"]
    print(classification_report(test_class_list, test_class_pred, target_names=target_names))

    # 保存模型
    save_mode(model_file, classifier, feature_words)
