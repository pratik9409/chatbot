import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
# nltk.download("punkt")

stemmer=PorterStemmer()

def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stemming(word):
    return stemmer.stem(word.lower())
    


def bagofwords(tokenized_sentence, all_words):
    tokenized_sentence = [stemming(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx]= 1.0
    return bag

# sentence = ["hello","how","are","you"]
# words = ["hi", "hello", "I", "you", "bye", "thank","cool"] 
# bag = bagofwords(sentence, words)
# print(bag)

