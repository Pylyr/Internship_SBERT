# Run sentence tokenization in parallel

from spacy.lang.en import English
from xml.sax import parse
from xml.sax.handler import ContentHandler
import re
import time
import tqdm


class XMLHandler(ContentHandler):
    def __init__(self, oFile):
        super().__init__()
        self.file = oFile  # output file
        self.curcmd = None  # current command
        self.currel = []  # current relations
        self.curwords = []  # current keywords
        self.texts = []  # texts of the abstracts (common relation)
        self.textc = 0  # current text

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
            if len(self.texts) > self.textc:
                self.texts[self.textc] += ' ' + content
            else:
                self.texts.append(content)

    def endElement(self, name):
        if name == "triple":
            self.textProcessing()
            self.currel = []
            self.texts = []
            self.textc = 0
        if name == "abs":
            self.textc += 1

    def textProcessing(self):
        global t0
        wordA, wordB = self.curwords
        wordA = wordA.replace("_", " ")
        wordB = wordB.replace("_", " ")

        processed_spacy = nlp.pipe(self.texts)
        processed_blocks = []
        sent_list = []
        # self.text = re.sub(r'\s+', ' ', self.text) # Not sure that is needed
        for doc in processed_spacy:
            sent_list.append([sent.text.strip() for sent in doc.sents])

        for sents in sent_list:
            sentA = []  # sentence containing wordA
            sentB = []  # sentence containing wordB
            sentAn = []  # sentence numbers containing wordA
            sentBn = []  # sentence numbers containing wordB
            sentence_counter = 0
            block = ""

            for sent in sents:
                if wordA in sent.casefold():
                    sentA.append(sent)
                    sentAn.append(sentence_counter)
                if wordB in sent.casefold():
                    sentB.append(sent)
                    sentBn.append(sentence_counter)
                sentence_counter += 1

            # if no sentences are found, return
            if len(sentA) == 0 or len(sentB) == 0:
                continue

            # Find the first common sentence between sentA and sentB
            for c in sentAn:
                if c in sentBn:
                    block = sents[c]
                    break

            if block:
                processed_blocks.append(block)
                continue  # we are done

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
                # length of sentences in sent_gen from start to end
                block_length = sum([len(sents[i]) for i in range(start, end + 1)])
                if block_length < best_block_length:
                    best_block_length = block_length
                    best_pair = [start, end]

            # extract the sentences in text from best_pair[0] to best_pair[1]
            block = ' '.join(sents[best_pair[0]:best_pair[1] + 1])

            if len(block) > 512:
                # block = "!!! Sentence too large !!!"
                continue

            processed_blocks.append(block)
        for block in processed_blocks:
            for rel in self.currel:
                # if there are double quotes in block, replace them with single quotes
                if '"' in block:
                    block = block.replace('"', "'")
                self.file.write(f"{wordA},{wordB},{rel},\"{block}\"\n")

        # t1 = time.time()
        # print(f"Wrote {len(processed_blocks) * len(self.currel)} lines in {t1 - t0} seconds")
        # t0 = t1
        pbar.update(n=1)


FILE = "./data/res1.xml"
LENGTH = 5000
# with open(FILE, 'r') as f:
#     LENGTH = len(re.findall(r'</triple>', f.read()))

nlp = English()
nlp.add_pipe("sentencizer")
t0 = time.time()

file = open("./data/processed.csv", "w")
file.write("Word A, Relation, Word B, Sentence\n")

handler = XMLHandler(file)


pbar = tqdm.tqdm(total=LENGTH)

parse(FILE, handler)
