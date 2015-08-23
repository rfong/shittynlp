import json
import os
from urllib import urlencode
import urllib2


vowels = 'aeiou'

def is_vowel(c):
  return len(c) == 1 and c in vowels

def is_consonant(c):
  return not is_vowel(c)


HYPHENATION_API = 'http://api.wordnik.com:80/v4/word.json/%s/hyphenation'

def get_syllables(word, dir='.'):
  path = os.path.join(dir, word + '.json')

  if not os.path.exists(dir):
    os.makedirs(dir)

  # If previously stored, read from file
  if os.path.exists(path):
    return json.loads(open(path, 'r').read())

  # Otherwise, query wordnik & save
  params = {
    'includeSuggestions': False,
    'api_key': '8d5d75f1783f5fa34407903328500b23d3357b2539f64eb9e',
    'useCanonical': False,
    'limit': 50,
  }
  url = '%s?%s' % (HYPHENATION_API % word, urlencode(params))
  data = urllib2.urlopen(url).read()
  f = open(path, 'w')
  f.write(data)
  f.close()
  return json.loads(data)
