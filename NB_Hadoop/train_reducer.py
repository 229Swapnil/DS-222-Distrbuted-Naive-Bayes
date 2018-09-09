import sys

(last_helper,last_key,count) = (None, None, 0)
for line in sys.stdin:
    (helper, key, value) = line.strip().split("\t")
    if last_helper == helper and last_key == key:
    	count += int(value)
    else:
    	if last_helper and last_key:
    		print("%s\t%s\t%s" % (last_helper,last_key,count))
    	(last_helper,last_key,count) = (helper, key, int(value))
print("%s\t%s\t%s" % (last_helper,last_key,count))
