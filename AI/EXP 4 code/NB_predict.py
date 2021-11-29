# encoding=utf-8
import pickle
import jieba
from sklearn.naive_bayes import MultinomialNB

model_file = "naive_bayes_model.m"
with open(model_file, "rb") as model_file:
    classifier = pickle.load(model_file)
    feature_words = pickle.load(model_file)
    print(feature_words)

    text = "特朗普下台啦"
    seged_text = jieba.cut(text)
    seged_text = list(seged_text)
    feature = [1 if word in seged_text else 0 for word in feature_words]
    print(feature)

    print(classifier.predict([feature]))
