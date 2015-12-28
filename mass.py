from collections import Counter
import time

_end = "_END"


def get_lexicon():
  return [w.strip().lower() for w in open("/usr/share/dict/words").readlines()]


class Trie():
  _trie = {}

  def path_exists(self, path):
    """Check if `path` in trie"""
    current_dict = self._trie
    for letter in path:
      if letter in current_dict:
        current_dict = current_dict[letter]
      else:
        return False
    else:
      if _end in current_dict:
        return True
      else:
        return False

  def get_paths(self, trie=None):
    """Run _get_paths() on a subtrie, or on the full trie by default."""
    if trie is None:
      trie = self._trie
    return self._get_paths(trie)

  @classmethod
  def _get_paths(cls, trie):
    """Return a list of all strings enumerated by a trie's paths."""
    strings = []
    for letter in trie:
      if letter == _end or isinstance(trie[letter], str):
        strings.append('')
      else:
        strings += [letter + leaf for leaf in cls._get_paths(trie[letter])]
    return strings

  def get_leaves(self, trie=None):
    """Run _get_leaves() on a subtrie, or on the full trie by default."""
    if trie is None:
      trie = self._trie
    return self._get_leaves(trie)
 
  @classmethod
  def _get_leaves(cls, trie):
    """Given a trie, get all values keyed to _END."""
    leaves = []
    for letter in trie:
      if letter == _end:
        leaves += trie[_end]
      else:
        leaves += cls._get_leaves(trie[letter])
    return leaves


class PrefixTrie(Trie):

  def __init__(self, words):
    self._trie = dict()
    for word in words:
      current_dict = self._trie
      for letter in word:
        current_dict = current_dict.setdefault(letter, {})
      current_dict[_end] = _end


class SubstringTrie(Trie):

  def __init__(self, words):
    """
    This fucker needs to know about the substring's original words, so instead
    of _END: _END let's put _END: [original word]
    """
    self._trie = dict()
    for word in words:
      for start in range(0, len(word)-1):
        current_dict = self._trie
        for letter in word[start:]:
          current_dict = current_dict.setdefault(letter, {})
        # This is ~5x faster than the concise non-in-place alternative
        if not current_dict.get(_end):
          current_dict[_end] = []
        current_dict[_end].append(word)

  def get_words_with_substring(self, substring):
    """Return words that contain `substring`"""
    curr = self._trie
    for letter in substring:
      curr = curr.get(letter, {})
    return self.get_leaves(curr)


def counter_avg(counter):
  """
  Given a counter with numerical keys of consistent type, return the weighted
  average of its keys.
  """
  return (sum(value * count for value, count in counter.iteritems()) /
          sum(counter.values()))


def most_common(counter, n, least=False, min_count=2):
  """Return the N most/least common keys in counter"""
  common = sorted(counter, key=counter.get, reverse=True)  # descending
  common = filter(lambda value: counter[value] >= min_count, common)
  if least:
    return common[-n:]
  return common[:n]


def main():
  start = time.time()
  lexicon = set(get_lexicon())
  print '%0.2f sec to fetch unix lexicon, %d words' % (
    time.time() - start, len(lexicon))
  print 'avg word length: %d' % counter_avg(Counter(len(w) for w in lexicon))

  start = time.time()
  prefix_trie = PrefixTrie(lexicon)
  print '%0.2f sec to make prefix trie, %d paths' % (
    time.time() - start, len(prefix_trie.get_paths()))

  start = time.time()
  substring_trie = SubstringTrie(lexicon)
  print '%0.2f sec to make substring trie, %d paths' % (
    time.time() - start, len(substring_trie.get_paths()))

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
  least_common_substrs = most_common(substring_counts, 1000, least=True)
  print most_common_substrs[:10]
  print least_common_substrs[:10]

  #print substring_trie['a']['a']['r']
  print substring_trie.get_words_with_substring('aar')
  print substring_trie.get_words_with_substring('ati')[:100]


#  import pandas
#  from collections import Counter
#  a = ['a', 'a', 'a', 'a', 'b', 'b', 'c', 'c', 'c', 'd', 'e', 'e', 'e', 'e', 'e']
#  letter_counts = Counter(a)
#  df = pandas.DataFrame.from_dict(letter_counts, orient='index')
#  df.plot(kind='bar')


if __name__ == '__main__':
  main()
