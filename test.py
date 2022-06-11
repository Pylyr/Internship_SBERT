
import timeit
import time
from spacy.lang.en import English
nlp = English()
nlp.add_pipe("sentencizer")


def testFunc():
    texts = ["I am not really sure where to go. It is so dark in here.",
             "Mom I told you many times it is not here. How do you want me to help you?"]

    texts *= 2

    sents = []
    for doc in nlp.pipe(texts):
        sents.append([sent.text for sent in doc.sents])

    return sents


# time the function testFunc() with timeit
# print(timeit.timeit(testFunc, number=100))

print(testFunc())
