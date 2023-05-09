
"""
USED FOR GENERATING THE DICTIONARY

DEPRECATED

"""

# importing libraries
from timeit import default_timer as timer

def load_words():
    with open('pen-1/words_alpha.txt') as word_file:
        valid_words = list(word_file.read().split())

    return valid_words

print('processing')
start = timer()
words = load_words()
with open('pen-1/dictionary.txt', 'w') as word_file:
    for word in words:
        if len(word) == 5:
            word_file.write(word+'\n')
end = timer()
 
print('finish at:', str(end - start))

# def save():
#     valid_words = []
#     with open('pen-1/dictionary.txt') as word_file:
#         valid_words = list(word_file.read().split())
#         word_file.close()
#     for word in valid_words:
#         trie.insert(word)

#     with open(r"pen-1/trie.dat", "wb") as output_file:
#         pickle.dump(trie, output_file)