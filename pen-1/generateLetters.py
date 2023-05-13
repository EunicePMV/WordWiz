from trie import *

class WordMastermind():

    def __init__(self, trie:Trie):
        # trie to check and get the valid word 
        self.trie = trie
        # get a word from the trie
        self.words_in_trie = []
        # container to get letters from that word
        self.pool_letters = []
        # final candidate 
        # should only append 5 candidates
        self.max_candidates = 5

    # get the sample stats
    def get_stats(self):
        pass


    # take the trie and search word from that 
    def search_word(self, node:TrieNode, depth = 0):
        word = ''
        if depth >= 5:
            return

        if len(self.words_in_trie) == self.max_candidates:
            return
        
        index = 0
        while index < 5:
            if node.nodes[index]:
                word += chr(97+index)
                if node.nodes[index].isWord == False:
                    self.search_word(self.words_in_trie, node.nodes[index], word)
                    word = word[0 : (len(word)-1)]
                else:
                    if word not in self.words_in_trie:
                        self.words_in_trie.append(word)
                    if 

    # to generate a least common word
    # search check the frequency of the letters if low 
    # then append to form a word
    # word append to candidate of words, then check there what word has the least score
    
    # get the word 
    # get the sample stats of that word



def getWordWithLowestScore():
    pass
    # check the frequency of letters in a word 
    # generate candidate