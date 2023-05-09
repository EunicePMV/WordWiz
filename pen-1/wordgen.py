from trie import *

class AIWordGenerator():
    
    """
    Initiates the word generator
        Takes in the Trie Dictionary, the pool of words, and the hints given to the codebreaker
    """
    def __init__(self, trie: Trie, pool: str, hints: dict) -> None:
        self.trie = trie
        self.pool = [letter for letter in pool]
        self.hints = hints
        self.pool_stack = []
        self.candidates = defaultdict(defaultValue)
        self.max_candidates = 5
        self.word = []
        self.attempts = []

    """
    get the candidate words and select the best one
    """
    def selectCandidate(self):
        if len(self.candidates) != 0:
            return max(self.candidates, key=self.candidates.get)
        return ""

    """
    scores the candidates by checking if the letter used was previously attempted or if the letter is given in the hint
    """
    def score(self):
        score = 0
        for word in self.attempts:
            for index in range(len(word)):
                if word[index] == self.word[index]:
                    score -= 2
        for index in range(len(self.word)):
            if self.hints[index] == self.word[index]:
                    score += 5
        return score
    
    """
    uses Modified DFS to find a word
    """
    def scrape(self, node: TrieNode = None, depth=0):
        #OPTIMISER HAX USAGE:
        used = False
        #FOR DEFEATING RIA
        """
        if max word length, return
        """
        if depth >= 5:
            return
        """
        randomizes the pool of words to get a variety of words to answer and iterate to each node
        """
        for letter in rd.sample(self.pool, len(self.pool)):
            """
            if a letter is hinted at the current depth and is not being used, try other letters
            """
            if self.hints[depth]:
                if letter != self.hints[depth]:
                    continue 
            """
            if maxed candidates is reached, return
            """
            if len(self.candidates) == self.max_candidates:
                return
            
            #OPTIMISER HAX:
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
            #FOR DEFEATING RIA

            """
            insert the letter in the word
            """
            self.word.append(letter)

            """
            if node holds a value, traverse it
            """
            if node.nodes[getLetterIndex(letter)]:
                """
                check if a word is found
                """
                if self.trie.search(self.convertWord()):
                    word = self.convertWord() 
                    """
                    append the word in the candidates if it not already a candidate or has not been attempted by the bot already
                    """
                    if word not in self.candidates and word not in self.attempts:
                        self.candidates[word] = self.score()

                """
                insert the letter used in the pool in a stack
                """
                self.pool_stack.append(self.pool.pop(self.pool.index(letter)))
                """
                search the child with used letter remove from the pool
                """
                self.scrape(node.nodes[getLetterIndex(letter)], depth+1)
                """
                retrive the letter from the stack once the letter is used
                """
                self.pool.append(self.pool_stack.pop(self.pool_stack.index(letter)))
            """
            letter is already used and can be removed
            """
            self.word.pop()

    """
    resets the candidates and updates the hints
    """
    def rethink(self, hints = None):
        print(self)
        if hints is not None:
            self.hints = hints
        self.candidates = defaultdict(defaultValue)
        
    """
    convert list to string
    """
    def convertWord(self):
        word = ""
        for letter in self.word: word += letter
        return word

    def __repr__(self) -> str:
        return (f'candidate: {self.selectCandidate()}\n'+
                f'candidates: {[candidate for candidate in self.candidates.items()]}\n' +
                f'attempts: {self.attempts}\n' +
                f'hints: {[hint for hint in self.hints.items()]}\n')
    
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
        ai.scrape(ai.trie.nodes)
        candidate = ai.selectCandidate()
        for index in range(len(candidate)):
            if word[index] == candidate[index]:
                hints[index] = word[index]
        
        ai.attempts.append(candidate)
        ai.rethink(hints)

        if candidate == word:
            print("------------------------------------")
            print(f'ANWSER: {candidate} | ATTEMPTS:{i+1}')
            print("------------------------------------")
            break    
        
    end = timer()
    print('finish at:', str(end - start))
