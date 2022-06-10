import re

sent_gen = (
    word
    for word
    in
    [
        "The use of mobile devices in combination with the rapid growth of the internet has generated an information overload problem.",
        "Recommender systems is a necessity to decide which of the data are relevant to the user.",
        "However in mobile devices there are different factors who are crucial to information retrieval, such as the location, the screen size and the processor speed.",
        "This paper gives an overview of the technologies related to mobile recommender systems and a more detailed description of the challenged faced."])

wordA = "information_overload"
wordB = "recommender_system"

wordA = wordA.replace("_", " ")
wordB = wordB.replace("_", " ")

sentA = []  # sentence containing wordA
sentB = []  # sentence containing wordB
sentAn = []  # sentence numbers containing wordA
sentBn = []  # sentence numbers containing wordB

block = ""
sentence_counter = 0
sents = [sent for sent in sent_gen]
for sent in sents:
    if re.search(wordA, sent, re.IGNORECASE):
        sentA.append(sent)
        sentAn.append(sentence_counter)
    if re.search(wordB, sent, re.IGNORECASE):
        sentB.append(sent)
        sentBn.append(sentence_counter)
    sentence_counter += 1

# generate all possible pairs of sentence indexes
pairs = []
for i in range(len(sentAn)):
    for j in range(len(sentBn)):
        pairs.append((sentAn[i], sentBn[j]))

# find the length of block that contains the sentences in pairs
best_block_length = 9999
best_pair = None
for pair in pairs:
    block_length = 0
    # length of sentences in sent_gen from pair[0] to pair[1]
    for i in range(pair[0], pair[1] + 1):
        block_length += len(sents[i])
    if block_length < best_block_length:
        best_block_length = block_length
        best_pair = pair

# extract the sentences in text from best_pair[0] to best_pair[1]
block = ""
for i in range(best_pair[0], best_pair[1] + 1):
    block += sents[i] + ' '


print(sentAn, sentBn)
print(best_pair)
print(block)
