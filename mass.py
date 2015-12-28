from collections import Counter
import time

_end = "_END"


def get_lexicon():
  return [w.strip().lower() for w in open("/usr/share/dict/words").readlines()]


class Trie():
  _trie = {}


class PrefixTrie(Trie):
  def __init__(self, words):
    self._trie = make_prefix_trie(words)


class SubstringTrie(Trie):
  def __init__(self, words):
    self._trie = make_substring_trie(words)


def make_prefix_trie(words):
  root = dict()
  for word in words:
    current_dict = root
    for letter in word:
      current_dict = current_dict.setdefault(letter, {})
    current_dict[_end] = _end
  return root


def make_substring_trie(words):
  """
  This fucker needs to know about the substring's original words, so instead
  of _END: _END let's put _END: [original word]
  """
  root = dict()
  for word in words:
    for start in range(0, len(word)-1):
      current_dict = root
      for letter in word[start:]:
        current_dict = current_dict.setdefault(letter, {})
      current_dict[_end] = current_dict.get(_end, []) + [word]
  return root


def in_trie(trie, word):
  """Check if `word` in `trie`"""
  current_dict = trie
  for letter in word:
    if letter in current_dict:
      current_dict = current_dict[letter]
    else:
      return False
  else:
    if _end in current_dict:
      return True
    else:
      return False


def get_trie_paths(trie):
  """Given a trie, return a list of all strings enumerated by its paths."""
  strings = []
  for letter in trie:
    if letter == _end or isinstance(trie[letter], str):
      strings.append('')
    else:
      strings += [letter + leaf for leaf in get_trie_paths(trie[letter])]
  return strings


def get_trie_leaves(trie):
  """Get all values keyed to _END in a trie."""
  leaves = []
  for letter in trie:
    if letter == _end:
      leaves.append(trie[_end])
    else:
      leaves += get_trie_leaves(trie[letter])
  return leaves


def get_words_with_substring(substring_trie, substring):
  """Given a substring trie, return strings that contain `substring`"""
  curr = substring_trie
  for letter in substring:
    curr = curr.get(letter, {})
  return get_trie_leaves(curr)


def counter_avg(counter):
  """
  Given a counter with numerical keys of consistent type, return the weighted
  average of its keys.
  """
  return (sum(value * count for value, count in counter.iteritems()) /
          sum(counter.values()))


def most_common(counter, n, reverse=True, min_count=2):
  """Return the N most/least common keys in counter"""
  common = sorted(counter, key=counter.get, reverse=(not reverse))
  return filter(lambda value: counter[value] >= min_count, common)[:n]


def main():
  start = time.time()
  lexicon = set(get_lexicon())
  print '%0.2f sec to fetch unix lexicon, %d words' % (
    time.time() - start, len(lexicon))
  print 'avg word length: %d' % counter_avg(Counter(len(w) for w in lexicon))

  start = time.time()
  prefix_trie = make_prefix_trie(lexicon)
  print '%0.2f sec to make prefix trie, %d paths' % (
    time.time() - start, len(get_trie_paths(prefix_trie)))

  start = time.time()
  substring_trie = make_substring_trie(lexicon)
  print '%0.2f sec to make substring trie, %d paths' % (
    time.time() - start, len(get_trie_paths(substring_trie)))

  MIN_SUBSTR_LEN = 3
  substrings = []
  start = time.time()
  for word in lexicon:
    for start_index in range(0, len(word) - 1):
      for end_index in range(start_index + MIN_SUBSTR_LEN, len(word)):
        substrings.append(word[start_index:end_index])
  substring_counts = Counter(substrings)
  print '%0.2f sec to tally substring counts' % (time.time() - start,)
  substring_len_counts = Counter([len(w) for w in substring_counts.keys()])

  most_common_substrs = most_common(substring_counts, 1000)
  least_common_substrs = most_common(substring_counts, 1000, reverse=True)
  print least_common_substrs[:10]

  print substring_trie['a']['a']['r']
  print get_words_with_substring(substring_trie, 'aar')


#  import pandas
#  from collections import Counter
#  a = ['a', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'c', 'd', 'e', 'e', 'e', 'e', 'e']
#  letter_counts = Counter(a)
#  df = pandas.DataFrame.from_dict(letter_counts, orient='index')
#  df.plot(kind='bar')


if __name__ == '__main__':
  main()
