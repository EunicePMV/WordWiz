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
