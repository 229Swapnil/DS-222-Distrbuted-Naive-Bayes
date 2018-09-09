import sys
import math

f = open("train_data", 'r')
label_word_count = {}
lines = f.readlines();
vocab_size = 0
for line in lines:
    line = line.strip()
    helper, label, count = line.split('\t')
    if(helper == "ANYLABEL"):
        label_word_count[label] = int(count)
    elif(helper == "ANYWORD"):
        vocab_size += 1
    else:
        break


smooth = 0.015
word_label_score = {}
index_label_score = {}
last_word = None
for line in sys.stdin:
	line = line.strip()
	word, label, count = line.split()
	word = word.strip()
	if word != "ANYLABEL" and word != "ANYWORD" and word != "APRIOR":
		if label in label_word_count:
			if last_word != word:
				word_label_score = {}
				last_word = word
			word_label_score[label] = math.log((int(count) + smooth)/(label_word_count[label] + smooth*vocab_size))
		else:
			if word_label_score:
				for l in label_word_count:
					if l in word_label_score:
						if label + '$'  + l in index_label_score:
							index_label_score[label + '$'  + l] += int(count)*word_label_score[l]
						else:
							index_label_score[label + '$'  + l] = int(count)*word_label_score[l]
					else:
						if label + '$'  + l in index_label_score:
							index_label_score[label + '$'  + l] += int(count)*math.log((smooth)/(label_word_count[l] + smooth*vocab_size))
						else:
							index_label_score[label + '$'  + l] = int(count)*math.log((smooth)/(label_word_count[l] + smooth*vocab_size))

for key in index_label_score:
    index, label = key.split('$')
    print('%s\t%s\t%.2f' % (index, label, index_label_score[key]))
