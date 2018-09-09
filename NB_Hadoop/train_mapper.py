import sys
import re

for doc in sys.stdin:
	doc = doc.lower().strip().split()
	labels = doc[0].split(",")
	doc = [re.sub(r'[^\w\s]','',word) for word in doc[3:] if re.sub(r'[^\w\s]','',word).isalpha() and len(re.sub(r'[^\w\s]','',word))>3]
	for label in labels:
		print("%s\t%s\t%s" % ("APRIOR",label,1))
		print("%s\t%s\t%s" % ("ANYLABEL",label,len(doc)))
    	for word in doc:
        	print("%s\t%s\t%s" % ("ANYWORD",word,1))
        	print("%s\t%s\t%s" % (word,label,1))