from optparse import OptionParser
import sys


vowels = 'aeiou'

def is_vowel(c):
  return len(c) == 1 and c in vowels

def is_consonant(c):
  return not is_vowel(c)


def indices(s, substr):
  '''Find indices of all occurrences of `substr` in `s`'''
  start = 0
  L = []
  while True:
    start = s.find(substr, start)
    if start < 0:
      break
    L.append(start)
    start += 1
  return L


def lcs(x, y):
  '''
  find longest common substrings with DP
  :returns: set of LCSs
  '''
  L = [[0]*len(y)]*len(x)
  longest = 0  # len of longest common substring found so far
  ret = set()  # strings of length `longest`
  for i in xrange(len(x)):
    for j in xrange(len(y)):
      if x[i] == y[j]:
        # update table
        if i == 0 or j == 0:
          L[i][j] = 1
        else:
          L[i][j] = L[i-1][j-1] + 1
        # found new best
        if L[i][j] > longest:
          longest = L[i][j]
          ret = set([ x[(i - longest + 1):i+1] ])
        elif L[i][j] == longest:
          ret.update(set([ x[(i - longest + 1):i+1] ]))
  return ret


def find_last_index(s, c):
  '''Find last index of char `c` in string `s`'''
  i = s[::-1].find(c)
  if i == -1:
    return -1
  return len(s) - i - 1


def join_near(x, y, join_on_vowel=True, reverse=False):
  '''join x to y on a vowel. order matters'''
  if reverse:
    (x,y) = (y,x)
  diff = len(x) + len(y)
  smush = None
  for i in xrange(len(y)):
    if is_vowel(y[i]) == join_on_vowel:
      char_i = find_last_index(x, y[i])
      if char_i > -1 and (len(x) - char_i + 1) < diff:
        diff = len(x) - char_i + i
        smush = x[:char_i] + y[i:]
  return smush


def first(listy, index=0, default=None):
  '''get if exists, else default'''
  if isinstance(listy, set):
    listy = list(listy)
  return listy[index] if len(listy) > index else default


def score(x, y, port, verbose=False):
  '''score portmanteau based on original words'''
  # TODO: ML this instead of jankily guessing weights yourself
  score = 0
  for word in [x, y]:
    # longest substring length up to 7
    ss_len = len(first(lcs(word, port), default=''))
    score += min(ss_len, 7)

  # penalize length > 12
  if len(port) > 12:
    score -= (len(port) - 12)

  # at least substr n>=3 represented from both
  if all(len(first(lcs(w, port), default='')) >= 3 for w in [x,y]):
    score += len(x+y) / 2

  # slight preference for order
  if port.startswith(x[:3]):
    score += 3

  return score


def smooth_join(x, y):
  '''
  joins while alternating vowels and consonants to make strings roll off
  the tongue. prioritize first string.
  '''
  if len(x) == 0 or len(y) == 0:
    return None
  if is_consonant(x[-1]):
    if is_consonant(y[0]):
      y = y[1:]
    return x + y
  return x + y


def join_on_substr(x, y, substr):
  '''
  Return all solutions of two strings joined on common substring.
  Works for multiple occurrences of `substr`.
  '''
  sslen = len(substr)
  solutions = set()
  # todo minimize dist
  for i in indices(x, substr):
    for j in indices(y, substr):
      # if substring is only one consonant from the end, incorporate it
      if i+sslen == len(x) - 1 and is_consonant(x[-1]):
        solutions.add(smooth_join(x[:i] + substr + x[-1], y[j+sslen:]))
      else:
        solutions.add(smooth_join(x[:i] + substr, y[j+sslen:]))
      if j+sslen == len(y) - 1 and is_consonant(y[-1]):
        solutions.add(smooth_join(y[:j] + substr + y[-1], x[i+sslen:]))
      else:
        solutions.add(smooth_join(y[:j] + substr, x[i+sslen:]))
  return solutions


def portmanteau(x, y, verbose=False):
  x = x.lower()
  y = y.lower()

  solutions = set()

  # Join on longest common substring
  substrs = list(lcs(x, y))
  # Remove standalone vowels
  substrs = [s for s in substrs if is_consonant(s)]
  #print 'substrings', substrs
  for substr in substrs:
    solutions.update(join_on_substr(x, y, substr))

  # Try joining along syllables near ends
  solutions.add(join_near(x, y))
  solutions.add(join_near(x, y, join_on_vowel=False))
  solutions.add(join_near(y, x))
  solutions.add(join_near(y, x, join_on_vowel=False))

  # TODO: this would be a lot better if we knew about syllable boundaries,
  # but detecting them is actually a phd thesis

  # Clean & print best
  solutions.discard(None)
  solutions.discard('')
  if verbose:
    for s in solutions:
      print s, score(x,y,s, verbose=verbose)
  return (max(solutions, key=lambda s: score(x,y,s, verbose=verbose))
          if solutions
          else None)


def main():
  parser = OptionParser()
  parser.add_option("-v", "--verbose", dest="verbose",
                    action="store_true", default=False,
                    help="print debug info")
  (options,args) = parser.parse_args()

  if len(args) == 2:
    print (portmanteau(args[0], args[1], verbose=options.verbose)
           or 'does not make a good portmanteau')

  # test barrage
  else:
    tests = [
      ('joshua', 'noah'),
      ('glen', 'noah'),
      ('brad', 'angelina'),
      ('tep', 'tetazoo'),
      ('beef', 'buffalo'),
      ('camel', 'leopard'),
      ('sheep', 'people'),
      ('california', 'fornication'),
      ('rock', 'documentary'),
      ('mock', 'documentary'),
      ('sacrilege', 'delicious'),
      ('literature', 'erotica'),
      ('scan', 'translation'),
      ('flavor', 'favorite'),
      ('mock', 'cocktail'),
      ('anachronism', 'acronym'),
      ('back', 'acronym'),
      ('bro', 'romance'),
      ('cocacola', 'colonization'),
      ('motor', 'cavalcade'),
      ('sex', 'expert'),
    ]
    for x, y in tests:
      port = portmanteau(x, y) or 'does not make a good portmanteau'
      print '%s + %s: %s' % (x, y, port)


if __name__ == '__main__':
  main()
