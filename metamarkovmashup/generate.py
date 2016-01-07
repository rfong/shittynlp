#!/usr/bin/env python -tt

from optparse import OptionParser
import pickle
import random
import sys

# Distribution across the two distinct chains
prob1 = 0.5
prob2 = 1.0 - prob1

def get_unigram_token():
  global bigram_chains
  chain = random.choice(bigram_chains)
  return random.choice(chain.keys())[0]

def get_bigram_token(token_tuple):
  """Pick next token with bigrams"""
  global bigram_chains
  next_options = [
    random.choice(chain[token_tuple])
    for chain in bigram_chains if token_tuple in chain]
  if not next_options:
    return None
  return random.choice(next_options)

def get_trigram_token(token_tuple):
  """Pick next token with trigrams"""
  global trigram_chains
  next_options = [
    random.choice(chain[token_tuple])
    for chain in trigram_chains if token_tuple in chain]
  if next_options:
    return random.choice(next_options)
  # No options. Fallback to bigrams.
  return get_bigram_token(token_tuple[-1])

def generate_bigram_sentence():
  sentence = []
  token = 'NOW'

  while True:
    next_token = get_bigram_token((token,))
    if not next_token:
      break
    token = next_token
    if token == 'END':
      break
    sentence.append(token)
  return ' '.join(sentence)

def generate_trigram_sentence():
  sentence = []
  (token1, token2) = ('BEGIN', 'NOW')

  while True:
    next_token = get_trigram_token((token1, token2))
    if not next_token:
      break
    token1, token2 = token2, next_token
    if token2 == "END":
      break
    sentence.append(token2)
  return ' '.join(sentence)

def main():
  parser = OptionParser()
  parser.add_option("-n", dest="num_sentences", default=1, type=int,
                    help="number of sentences to generate")
  (options, args) = parser.parse_args()

  global bigram_chains, trigram_chains
  bigram_chains = [pickle.load(open('%s.%dchain' % (fname, 2), 'rb'))
                   for fname in args]
  trigram_chains = [pickle.load(open('%s.%dchain' % (fname, 3), 'rb'))
                   for fname in args]

  for i in xrange(options.num_sentences):
    print generate_trigram_sentence()


if __name__ == '__main__':
  main()
