import sys
import re

for doc in sys.stdin:
	doc = doc.lower().strip().split()
	index = doc[0]
	doc = [re.sub(r'[^\w\s]','',word) for word in doc[4:] if re.sub(r'[^\w\s]','',word).isalpha() and len(re.sub(r'[^\w\s]','',word))>3]
	for word in doc:
		print("%s\t%s\t%s" % (word + " ", index, 1))