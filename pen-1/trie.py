import pickle, random as rd
from typing import List
from typing import List
from timeit import default_timer as timer
from collections import defaultdict

#For reference
alpha = 'abcdefghijklmnopqrstuvwxyz'

#Get index of letter
def getLetterIndex(letter):
    return ord(letter) - ord('a')

#Default value of dictionaries without values
def defaultValue():
    return None

#Node of Trie
class TrieNode():
    #Initiates the Node with 26 None values representing each letter
    def __init__(self):
        self.nodes:List[TrieNode | None] = [None for _ in range(26)]
        self.isWord = False
    
    #Gets the frequency or how many times this letter had been used in a particular word given its depth in the Trie
    def frequency(self):
        freq = 0
        for i in self.nodes:
            if i is not None:
                freq += 1
        return freq

#Trie
class Trie():
    #assigns the initial alphabet
    def __init__(self):
        self.nodes = TrieNode()

    #insert a word in the Trie
    def insert(self, word):
        node: TrieNode = self.nodes
        nodes = node.nodes
        for letter in word:
            nodeIndex = ord(letter) - ord('a')
            if nodes[nodeIndex] is None:
                nodes[nodeIndex] = TrieNode()
            node = nodes[nodeIndex]
            nodes = node.nodes

        node.isWord = True 

    #search for word in Trie
    def search(self, word):
        node: TrieNode = self.nodes
        nodes = node.nodes
        for letter in word:
            nodeIndex = ord(letter) - ord('a')
            if nodes[nodeIndex] is None:
                nodes[nodeIndex] = TrieNode()
            node = nodes[nodeIndex]
            nodes = node.nodes
            
        return node.isWord
    
    #load values given that the Trie is saved
    def load(self):
        with open(r"pen-1/trie.dat", "rb") as input_file:
            trie:Trie = pickle.load(input_file)
            self.nodes = trie.nodes
            input_file.close()
    
    #save the Trie object into a dat file
    def save(self):
        valid_words = []
        with open('pen-1/dictionary.txt') as word_file:
            valid_words = list(word_file.read().split())
            word_file.close()
        for word in valid_words:
            self.insert(word)

        with open(r"pen-1/trie.dat", "wb") as output_file:
            pickle.dump(self, output_file)