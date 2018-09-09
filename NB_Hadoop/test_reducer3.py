import sys
import math

f = open("train_data", 'r')
label_count = {}
lines = f.readlines()
for line in lines:
    line = line.strip()
    helper, label, count = line.split('\t')
    if helper == "APRIOR":
        label_count[label] = int(count)     
    elif helper != "ANYLABEL" and helper != "ANYWORD":
        break

total = sum(label_count.values())

for key in label_count:
    label_count[key] = label_count[key]/total


index_predict = {}
last_index = None
for line in sys.stdin:
    line = line.strip()
    index, label, score = line.split('\t')
    score = float(score) + math.log(label_count[label])
    if index != last_index:
        last_index = index
        max_score = score
        index_predict[index] = label
    else:
        if score > max_score:
            max_score = score
            index_predict[index] = label


for key in index_predict:
    print("%s\t%s" % (key,index_predict[key]))
