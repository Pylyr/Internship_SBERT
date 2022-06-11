from spacy.lang.en import English
from xml.sax import parse
from xml.sax.handler import ContentHandler
import re
import time


nlp = English()
nlp.add_pipe("sentencizer")


t0 = time.time()


class XMLHandler(ContentHandler):
    def __init__(self, oFile):
        super().__init__()
        self.file = oFile  # output file
        self.curcmd = None  # current command
        self.currel = []  # current relations
        self.curwords = []  # current keywords
        self.text = ""  # text of the abstract

    def startElement(self, name, attrs):
        self.curcmd = name
        if name == "triple":
            self.curwords = [attrs.getValue("e1"), attrs.getValue("e2")]

    def characters(self, content):
        if content.isspace():
            return
        if self.curcmd == "r":
            if not content.endswith("By"):
                self.currel.append(content)
        elif self.curcmd == "abs":
            self.text += ' ' + content

    def endElement(self, name):
        if name == "triple":
            self.currel = []
        if name == "abs":
            self.textProcessing()
            self.text = ""

    def textProcessing(self):
        wordA, wordB = self.curwords
        # some preprocessing
        wordA = wordA.replace("_", " ")
        wordB = wordB.replace("_", " ")
        self.text = re.sub(r'\s+', ' ', self.text)
        self.text = self.text.strip()

        sentA = []  # sentence containing wordA
        sentB = []  # sentence containing wordB
        sentAn = []  # sentence numbers containing wordA
        sentBn = []  # sentence numbers containing wordB

        block = ""
        sentence_counter = 0
        doc = nlp(self.text)

        sents = [sent.text.strip() for sent in doc.sents]
        for sent in sents:
            if re.search(wordA, sent, re.IGNORECASE):
                sentA.append(sent)
                sentAn.append(sentence_counter)
            if re.search(wordB, sent, re.IGNORECASE):
                sentB.append(sent)
                sentBn.append(sentence_counter)
            sentence_counter += 1

        # if no sentences are found, return
        if len(sentA) == 0 or len(sentB) == 0:
            return

        # Find the first common sentence between sentA and sentB
        for c in sentAn:
            if c in sentBn:
                block = sents[c]
                break

        if block:
            for rel in self.currel:
                self.file.write(f"{wordA},{wordB},{rel},\"{block}\"\n")
            return  # we are done

        # generate all possible pairs of sentence indexes
        pairs = []
        for i in range(len(sentAn)):
            for j in range(len(sentBn)):
                pairs.append((sentAn[i], sentBn[j]))

        # Find the shortest block that contains the sentences in pairs
        # This is not very efficient, but it works
        best_block_length = 9999
        best_pair = None
        for pair in pairs:
            start = min(pair)  # Because sentences can be in the wrong order
            end = max(pair)
            block_length = 0
            # length of sentences in sent_gen from start to end
            for i in range(start, end + 1):
                block_length += len(sents[i])
            if block_length < best_block_length:
                best_block_length = block_length
                best_pair = [start, end]

        # extract the sentences in text from best_pair[0] to best_pair[1]
        block = ""
        for i in range(best_pair[0], best_pair[1] + 1):
            block += sents[i] + ' '
        if len(block) < 512:
            for rel in self.currel:
                self.file.write(f"{wordA},{wordB},{rel},\"{block}\"\n")


file = open("./data/processed.csv", "w")
file.write("Word A, Relation, Word B, Sentence\n")

handler = XMLHandler(file)
parse("./data/test1000.xml", handler)

t1 = time.time()
print(t1-t0)
