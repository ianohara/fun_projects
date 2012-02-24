from datastructures.Trie import Trie

class ElBotTrie(Trie):
    def __init__(self):
        Trie.__init__(self)
    
    def add_sentence(self, sentence):
        for word in sentence.split(' '):
            self.add_word(word)
        return True
"""
    def total_words(self):
        for n in self.subtree_iterator(self.root):
            print n.end_count

    def subtree_iterator(self, node):
        for child_name in node.children.keys():
            if not node.children[child_name]:
                continue
            print node
            print 'Going deeper in the iter tree at child %s.' % child_name
            self.subtree_iterator(node.children[child_name])
        yield node
"""
    def count(self, unsafe_word):
        word = self.make_safe(unsafe_word)
        return self._count(self.root, word)

    def _count(self, node, word):
        if not word:
            raise RuntimeError
        if not node.children[word[0]]:
            return 0
        elif len(word) is 1:
            return node.children[word[0]].end_count
        else:
            return self._count(node.children[word[0]], word[1:])
