import json
import random

MIN_SCORE = 229
MAX_SYLLABLES = 3

if __name__=='__main__':
  rhymes = {}
  for word in ['cherry', 'pickle']:
    rhymes[word] = json.loads(open(word + '.json', 'r').readline())['rhymes']
    rhymes[word] = filter(
      lambda w: (w['score'] >= MIN_SCORE and
                 int(w['syllables']) <= MAX_SYLLABLES),
      rhymes[word])

  for i in xrange(20):
    rhyme = [
      random.choice(rhyme_set)['word'] for rhyme_set in rhymes.values()]
    random.shuffle(rhyme)
    print ''.join(rhyme)
