#!/usr/bin/env python -tt

import pickle
import os
import re
import sys


def yield_ngram(words, n):
  if len(words) < n:
    return
  for i in xrange(len(words) - (n - 1)):
    yield tuple(words[i:i+n])

def get_tokens(s):
  #return re.findall(r"[\w']+", s)
  return s.split()

def build_ngram_chain(file, n):
  chain = {}
  for line in file:
    words = get_tokens(line)
    for word_tuple in yield_ngram(words, n):
      key = word_tuple[:-1]
      if key in chain:
        chain[key].append(word_tuple[-1])
      else:
        chain[key] = [word_tuple[-1]]
  return chain


if __name__ == '__main__':
  fname = sys.argv[1]
  for n in [2,3]:
    f = open(fname, 'r')
    chain = build_ngram_chain(f, n)
    out_name = os.path.splitext(sys.argv[1])[0] + '.%dchain' % n
    pickle.dump(chain, open(out_name, 'wb'))
