_end = "_END"


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


class SuffixTrie(PrefixTrie):

  def __init__(self, words):
    """
    Needs to know about substring's original words, so store _END: [words].
    Store paths in reverse for simplified construction.
    """
    self._trie = dict()
    for word in words:
      current_dict = self._trie
      for letter in reversed(word):
        current_dict = current_dict.setdefault(letter, {})
      if not current_dict.get(_end):
        current_dict[_end] = []
      current_dict[_end].append(word)

  def path_exists(self, path):
    return super(SuffixTrie, self).path_exists(reversed(path))

  def get_paths(self, trie=None):
    return [list(reversed(word)) for word in
            super(SuffixTrie, self).get_paths(self, trie=None)]

  def fetch(self, suffix):
    """Return words ending in `suffix`"""
    curr = self._trie
    for letter in reversed(suffix):
      curr = curr.get(letter, {})
    return self.get_leaves(curr)

  @staticmethod
  def _reverse_all(words):
    return (reversed(word) for word in words)


class SubstringTrie(Trie):

  def __init__(self, words):
    """
    This little fucker needs to know about the substring's original words, so
    instead of _END: _END let's put _END: [original word]
    """
    self._trie = dict()
    for word in words:
      for start in range(0, len(word)-1):
        current_dict = self._trie
        for letter in word[start:]:
          current_dict = current_dict.setdefault(letter, {})
        # This is ~5x faster than the non-in-place oneliner option
        if not current_dict.get(_end):
          current_dict[_end] = []
        current_dict[_end].append(word)

  def fetch(self, substring):
    """Return words that contain `substring`"""
    curr = self._trie
    for letter in substring:
      curr = curr.get(letter, {})
    return self.get_leaves(curr)
