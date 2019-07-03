

# https://github.com/monisjaved/Data-Processing-With-Hadoop/tree/master/Code/Lab4-2
from pyspark.sql import SparkSession
import string


# Lower and Clean a string
def lower_clean_str(x):
  punc='!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
  lowercased_str = x.lower()
  for ch in punc:
    lowercased_str = lowercased_str.replace(ch, '')
  return lowercased_str


# Read a text file, split it to words, get unique values, lower words and remove punctuation, filter out duplicate word generated, sort the result
def get_sorted_words(text_file_name):
   v_document = spark.read.text(text_file_name).rdd.map(lambda r :r[0])
   sortedCount = v_document.flatMap(lambda x: x.split(' ')).distinct().map(lambda x : lower_clean_str(x)).distinct().map(lambda x : (x,1)).sortByKey()
   output = sortedCount.collect()
	
   words = []
   for (c_word, unitcount) in output:
      words.append(c_word)

   return words



spark = SparkSession\
        .builder\
        .appName("gkl_word_cooccurrences")\
        .getOrCreate()

# Read file and return the ordered word list
sorted_words = get_sorted_words("texte1.txt")
print(sorted_words)

# Option : remove stop words
# stop_word_list = ['a', "une", ...]
# rdd =  rdd.filter(lambda x : x not in stop_word_list)
# rdd.take()


# Build pairs
pairs_list=[]
for i in range(1, len(sorted_words)-1, 1):
        for j in range(i+1,len(sorted_words)):
             pairs_list.append("%s|%s###%s" % (sorted_words[i],sorted_words[j], 1))


# Reduce
current_word = None
current_count = 0
word = None

for pair_list in pairs_list:
    
     
    wordpair, count = pair_list.split('###', 1)
    count = int(count)

    if current_word == wordpair:
        current_count += count
    else:
        current_count = count
        current_word = wordpair





spark.stop()

