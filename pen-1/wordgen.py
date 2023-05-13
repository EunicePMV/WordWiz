from trie import *

class AIWordGenerator():
    
    def __init__(self, trie: Trie, pool: str, hints: dict) -> None:
        self.trie = trie
        self.pool = [letter for letter in pool]
        self.hints = hints
        self.pool_stack = []
        self.candidates = defaultdict(defaultValue)
        self.globalScore = 0
        self.max_candidates = 5
        self.word = []
        self.attempts = defaultdict(defaultValue)

    def selectCandidate(self):
        if len(self.candidates) != 0:
            return max(self.candidates, key=self.candidates.get)
        return ""

    def localScore(self):
        localScore = 0
        for word in self.attempts:
            for index in range(len(word)):
                if word[index] == self.word[index]:
                    localScore -= 5
        for index in range(len(self.word)):
            if self.hints[index] == self.word[index]:
                    localScore += 15
        return localScore + self.globalScore/2
    
    def getSampleStats(self, node: TrieNode):
        for letter in self.pool:
            if node.nodes[getLetterIndex(letter)]:
                print(f'{letter}: {node.nodes[getLetterIndex(letter)].frequency()} ')
            else:
                print(f'{letter}: {0} ')
        print()

    def search(self, node: TrieNode = None, depth=0):
        # self.getSampleStats(node)
        used = False
        if depth >= 5:
            return
        for letter in rd.sample(self.pool, len(self.pool)):
            if self.hints[depth]:
                if letter != self.hints[depth]:
                    continue 
            if len(self.candidates) == self.max_candidates:
                return
            
            for word in self.attempts:
                if word and self.hints[depth]:
                    if word[depth] == letter and self.hints[depth] != word[depth]:
                        used = True
                else:
                    if word:
                        if word[depth] == letter:
                            used = True
            if used:
                used = False
                continue

            self.word.append(letter)     
            current_node = node.nodes[getLetterIndex(letter)]
            self.globalScore += current_node.frequency() if current_node is not None else 0
            if current_node:  
                          
                if self.trie.search(self.convertWord()):
                    word = self.convertWord() 
                    # print("word: ", word)
                    if word not in self.candidates and word not in self.attempts:
                        self.candidates[word] = self.localScore()
                    # print("candidates101: ", self.candidates)
                self.pool_stack.append(self.pool.pop(self.pool.index(letter)))
                # print("pool: ", self.pool)
                # print("pool_stack: ", self.pool_stack)
                self.search(current_node, depth+1)
                self.pool.append(self.pool_stack.pop(self.pool_stack.index(letter)))
                # print("pool_stack: ", self.pool_stack)
                # print("pop this letter: ", self.pool_stack.index(letter))
            self.globalScore -= current_node.frequency() if current_node is not None else 0
            self.word.pop()
            

    def stats(self):
        print(self)

    def think(self):
        self.search(self.trie.nodes)
        return self.selectCandidate()

    def rethink(self, hints = None):
        if hints is not None:
            self.hints = hints
        self.candidates = defaultdict(defaultValue)
        
    def convertWord(self):
        word = ""
        for letter in self.word: word += letter
        return word

    def __repr__(self) -> str:
        return (f'candidate: {self.selectCandidate()}\n'+
                f'candidates: {[candidate for candidate in self.candidates.items()]}\n' +
                f'attempts: {[attempt for attempt in self.attempts.items()]}\n' +
                f'hints: {"".join([hint if hint is not None else "_" for hint in self.hints.values()])}\n')
    
def sample(word = None, pool = None):
    start = timer()

    trie = Trie()
    # trie.save()
    trie.load()
    word = "glass" if word is None else word
    pool = "gonianless" if pool is None else pool
    hints = defaultdict(defaultValue)

    ai = AIWordGenerator(trie, pool, hints)
    print("\n---STATS---\n")
    for i in range(6):
        
        candidate = ai.think()
        for index in range(len(candidate)):
            if word[index] == candidate[index]:
                hints[index] = word[index]
        
        ai.attempts[candidate] = ai.candidates[candidate]
        ai.stats()
        ai.rethink(hints)

        if candidate == word:
            print("------------------------------------")
            print(f'ANWSER: {candidate} | ATTEMPTS:{i+1}')
            print("------------------------------------")
            break    
        
    end = timer()
    print('finish at:', str(end - start))


# Mastermind Pseudocode:

# Input:
# 	node: Node in a Trie
# 	depth: The current recursion depth

# Output:
# 	[word, score] -> dictionary of words with a given score

# Procedure:
# FUNCTION search(node, depth):
# 	if depth >= 5: 
# 		return
# 	for all letters in the pool of letter:
# 		if max candidates is reached:
# 			return
# 		word -> add letter to word
# 		current node -> the child node representation of letter
# 		score -> add frequency of letter

# 		if current node is not empty
# 			 if current word is valid
# 				if word is not attempted and is not a candidate
# 					add word to candidates and score
# 			add the current letter to stack
# 			search(current node, depth+1)
# 			retrieve the current letter from stack


# FUNCTION getWordWithLowestScore([word, score])
# 	return word with lowest sore
