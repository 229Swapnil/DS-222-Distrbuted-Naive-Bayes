hadoop fs -rm -r /user/swapnilgupta.229/gupta/train_output/
hadoop fs -rm -r /user/swapnilgupta.229/gupta/test_output/
hadoop fs -rm -r /user/swapnilgupta.229/gupta/score_out/
hadoop fs -rm -r /user/swapnilgupta.229/gupta/predict_out/

hadoop fs -rm /user/swapnilgupta.229/gupta/train_out_m_s.txt
hadoop fs -rm /user/swapnilgupta.229/gupta/score_out_m_s.txt
hadoop fs -rm /user/swapnilgupta.229/gupta/concat.txt

rm -r /home/swapnilgupta.229/Ass1/train_out
rm -r /home/swapnilgupta.229/Ass1/test_out
rm -r /home/swapnilgupta.229/Ass1/score_out
rm -r /home/swapnilgupta.229/Ass1/predict_out

rm /home/swapnilgupta.229/Ass1/concat.txt
rm /home/swapnilgupta.229/Ass1/predict_out_m.txt

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D stream.map.output.field.separator='\t'  -D stream.num.map.output.key.fields=2 -D mapred.text.key.partitioner.options=-k1,2 -files /home/swapnilgupta.229/Ass1/train_mapper.py,/home/swapnilgupta.229/Ass1/train_reducer.py -input /user/swapnilgupta.229/ass1/full_train.txt -output /user/swapnilgupta.229/gupta/train_output/ -mapper "python3 /home/swapnilgupta.229/Ass1/train_mapper.py" -reducer "python3 /home/swapnilgupta.229/Ass1/train_reducer.py"

hadoop fs -cat /user/swapnilgupta.229/gupta/train_output/* > /home/swapnilgupta.229/Ass1/train_out.txt

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar -D stream.map.output.field.separator='\t'  -D stream.num.map.output.key.fields=2 -D mapred.text.key.partitioner.options=-k1,2 -files /home/swapnilgupta.229/Ass1/test_mapper1.py,/home/swapnilgupta.229/Ass1/train_reducer.py -input /user/swapnilgupta.229/ass1/full_test_id.txt -output /user/swapnilgupta.229/gupta/test_output/ -mapper "python3 /home/swapnilgupta.229/Ass1/test_mapper1.py" -reducer "python3 /home/swapnilgupta.229/Ass1/train_reducer.py"

hadoop fs -cat /user/swapnilgupta.229/gupta/test_output/* > /home/swapnilgupta.229/Ass1/test_out.txt
cat /home/swapnilgupta.229/Ass1/train_out.txt /home/swapnilgupta.229/Ass1/test_out.txt > /home/swapnilgupta.229/Ass1/concat.txt
hadoop fs -put /home/swapnilgupta.229/Ass1/concat.txt /user/swapnilgupta.229/gupta/

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar  -D stream.map.output.field.separator='\t'  -D stream.num.map.output.key.fields=2 -D mapred.text.key.partitioner.options=-k1,1 -files /home/swapnilgupta.229/Ass1/test_mapper2.py,/home/swapnilgupta.229/Ass1/test_reducer2.py -input /user/swapnilgupta.229/gupta/concat.txt -output /user/swapnilgupta.229/gupta/score_out/ -mapper "python3 /home/swapnilgupta.229/Ass1/test_mapper2.py" -reducer "python3 /home/swapnilgupta.229/Ass1/test_reducer2.py" -cacheFile /user/swapnilgupta.229/gupta/train_output/part-00000#train_data

hadoop jar /usr/hdp/current/hadoop-mapreduce-client/hadoop-streaming.jar  -D stream.map.output.field.separator='\t'  -D stream.num.map.output.key.fields=2 -D mapred.text.key.partitioner.options=-k1,1 -files /home/swapnilgupta.229/Ass1/test_mapper2.py,/home/swapnilgupta.229/Ass1/test_reducer3.py -input /user/swapnilgupta.229/gupta/score_out/* -output /user/swapnilgupta.229/gupta/predict_out/ -mapper "python3 /home/swapnilgupta.229/Ass1/test_mapper2.py" -reducer "python3 /home/swapnilgupta.229/Ass1/test_reducer3.py" -cacheFile /user/swapnilgupta.229/gupta/train_output/part-00000#train_data

hadoop fs -cat /user/swapnilgupta.229/gupta/predict_out/* > /home/swapnilgupta.229/Ass1/predict_out.txt