"""
A trie implementation (originally for elBot)
by: Ian O'Hara, 2012
"""
import logging as log

class Node():
    def __init__(self, parent, 
            children_names='a b c d e f g h i j k l m n o p q r s t u v w x y z', 
            my_name=None):
        self.my_name = my_name;
        self.parent = parent
        self.children_names = children_names
        self.children = dict(zip([ch for ch in self.children_names.split(' ') if ch],
                                 (None for dummy in xrange(len(self.children_names)))))
        self.end_count = 0 # Number of entries that have ended at this node

class Trie():
    strip_chars = '1234567890 ,<>./?\'";:\\|]}[{=+-_)(*&^%$#@!~`'
    def __init__(self, _DEBUG=False):
        if _DEBUG:
            log.basicConfig(level=log.DEBUG)
        self.root = Node(None)
    
    @classmethod
    def make_safe(cls, word):
        word = word.translate(None, Trie.strip_chars)
        word = word.lower()
        return word

    def add_word(self, unsafe_word):
        word = Trie.make_safe(unsafe_word)
        if not word:
            return
        #print('Adding a new word "%s" (unsafe form: "%s")' % (word, unsafe_word))
        self._add_safe_word(self.root, word)
        return True

    def _add_safe_word(self, node, word):
        """Reached the end of the word, so make sure the end node exists
           and then increment the word end count of this node.
        """
        if len(word) is 1:
            if not node.children[word]:
                #print('Adding new word end...')
                node.children[word] = Node(parent=node, my_name=word)
            node.children[word].end_count += 1
            #print('Word end with count %d.' % node.children[word].end_count)
            return
        elif len(word) > 1:
            if not node.children[word[0]]:
                node.children[word[0]] = Node(parent=node, my_name=word[0])
            #print('Going deeper...')
            self._add_safe_word(node.children[word[0]], word[1:])
        else:
            raise RuntimeWarning # We shouldn't ever reach this...


