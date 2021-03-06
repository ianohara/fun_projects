from datastructures.Trie import Trie

class ElBotTrie(Trie):
    def __init__(self):
        Trie.__init__(self)
    
    def add_sentence(self, sentence):
        for word in sentence.split(' '):
            self.add_word(word)
        return True

    def get_word_dict(self):
        return self._subtree_dict(self.root)

    def _subtree_dict(self, node, accum_word='', accum_dict={}):
        # The root node has no letter assigned to it
        if node.my_name:
            accum_word += node.my_name
        # Might be at a non-word ending letter, this also
        # takes care of the root node
        if node.end_count:
            print 'accum: %s at letter: %s end count is %d' % (accum_word, node.my_name, node.end_count)
            accum_dict[accum_word] = node.end_count
        for next_node in node.children.itervalues():
            if next_node is not None:
                accum_dict = self._subtree_dict(next_node, accum_word, accum_dict)
        return accum_dict

    def total_words(self):
        return self._subtree_words(self.root)

    def _subtree_words(self, node, accum=0):
        accum += node.end_count
        for next_node in node.children.itervalues():
            if next_node is not None:
               accum = self._subtree_words(next_node, accum=accum)
        return accum

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
