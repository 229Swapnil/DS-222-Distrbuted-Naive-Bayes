import numpy as np
import time
import re
from collections import Counter


train_path='./DBPedia.full/full_train.txt'
test_path='./DBPedia.full/full_test.txt'
devel_path='./DBPedia.full/full_devel.txt'

def _train(file_path):
    file = open(file_path,'r')
    file = file.readlines()
    data = {}
    y_data = {}
    vocab = []
    total_class = 0
    for doc in file:
        doc = doc.lower().strip().split()
        labels = doc[0].split(",")
        doc = [re.sub(r'[^\w\s]','',word) for word in doc[3:] if re.sub(r'[^\w\s]','',word).isalpha() and len(word)>3]
        doc = Counter(doc)
        vocab += list(doc.keys())
        for label in labels:
            total_class += 1
            if label in y_data:
                (total_words,y_freq) = y_data[label]
                total_words += sum(doc.values())
                y_freq += 1
                y_data[label] = (total_words,y_freq)
            else:
                y_data[label] = (sum(doc.values()),1)
            for word in doc:
                if word + "^" + label in data:
                    data[word + "^" + label] += doc[word]
                else:
                    data[word + "^" + label] = doc[word]
    return data,y_data,set(vocab),total_class

def read_test_data(file_path,vocab):
    file = open(file_path,'r')
    file = file.readlines()
    data = []
    labels = []
    test_vocab = []
    for doc in file:
        doc = doc.lower().strip().split()
        labels.append(doc[0].split(","))
        doc = [re.sub(r'[^\w\s]','',word) for word in doc[3:] if re.sub(r'[^\w\s]','',word) in vocab]
        doc = Counter(doc)
        test_vocab += list(doc.keys())
        data.append(doc)
    return data,labels,set(test_vocab)

def get_prob(train_data,y_data,test_vocab,vocab_size,smooth):
    for word in test_vocab:
        for y in y_data:
            if word + "^" + y in train_data:
                train_data[word+"^"+y] = np.log((train_data[word+"^"+y] + smooth)/(y_data[y][0] + vocab_size*smooth))
    return train_data

def get_test_score(doc,y,train_data,y_data,vocab_size,smooth,total_class):
    score = 0
    for word in doc:
        if word + "^" + y in train_data:
            score += doc[word]*train_data[word + "^" + y]
        else:
            score += doc[word]*(np.log(smooth/(y_data[y][0] + vocab_size*smooth)))                
    score += np.log(y_data[y][1]/total_class)
    return score

def get_accuracy(test_data,test_labels,train_data,y_data,vocab_size,smooth,total_class):
    count = 0
    y_list = list(y_data.keys())
    for i,doc in enumerate(test_data):
        score = [get_test_score(doc,y,train_data,y_data,vocab_size,smooth,total_class) for y in y_list]
        label = y_list[np.argmax(score)]
        if label in test_labels[i]:
            count += 1
    return count/len(test_data)


### Training Phase
start = time.time()
train_data, y_data, vocab, total_class = _train(train_path)
print("train_time: %s seconds" % (time.time() - start))

### Testing Phase
start = time.time()
test_data, test_labels, test_vocab = read_test_data(test_path,vocab)
smooth = 0.015
train_data_proc = get_prob(train_data,y_data,test_vocab,len(list(vocab)),smooth)
acc = get_accuracy(test_data,test_labels,train_data_proc,y_data,len(list(vocab)),smooth,total_class)
print("test_time: %s seconds" % (time.time() - start))
print("test_accuracy: ",acc)

