from collections import Counter
import time

from trie import PrefixTrie
from trie import SubstringTrie
from trie import SuffixTrie


def get_lexicon():
  return [w.strip().lower() for w in open("/usr/share/dict/words").readlines()]


def counter_avg(counter):
  """
  Given a counter with numerical keys of consistent type, return the weighted
  average of its keys.
  """
  return (sum(value * count for value, count in counter.iteritems()) /
          sum(counter.values()))


def most_common(counter, n=1, least=False, min_count=2):
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

  # We'll be lazy and make a suffix trie by using reverse words and reverse
  # lookup paths
  suffix_trie = SuffixTrie(lexicon)

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

  most_common_substrs = most_common(substring_counts, n=10)
  least_common_substrs = most_common(substring_counts, n=10, least=True,
                                     min_count=10)
  print most_common_substrs
  print least_common_substrs

  print substring_trie.fetch('aar')
  print substring_counts['aar']
  print substring_trie.fetch('ati')[:100]
  print substring_trie.fetch('tillatio')
  print substring_trie.fetch('naest')
  print substring_trie.fetch('nctil')


if __name__ == '__main__':
  main()
