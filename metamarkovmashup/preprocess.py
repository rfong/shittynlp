from nltk import tokenize
import os
import sys
import unicodedata

file_name = sys.argv[1]
file = open(file_name, 'r')
out_name = os.path.splitext(file_name)[0] + '.sentences'
out = open(out_name, 'w')

# Let's lazily assume everything fits in memory with no problems
text = unicodedata.normalize('NFKD', file.read().decode('utf-8')).encode('ascii', 'ignore')
for sentence in tokenize.sent_tokenize(text):
  out.write('BEGIN NOW %s END\n' % sentence.strip())

file.close()
out.close()
