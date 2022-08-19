# Run sentence tokenization in parallel

from spacy.lang.en import English
from xml.sax import parse
from xml.sax.handler import ContentHandler
import time
import tqdm
import re
import os
import inflect

N = 370 # Maximum number of characters allowed in a block.

def is_well_parenthesized(string):
    stack = 0
    for char in string:
        if char == "(":
            stack += 1
        elif char == ")":
            if stack == 0:
                return False
            stack -= 1
    return stack == 0

class XMLHandler(ContentHandler):
    def __init__(self, output_file):
        super().__init__()
        self.file = output_file  # output file
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

        if not is_well_parenthesized(wordA) or not is_well_parenthesized(wordB):
            return
        
        try:
            wordApl = p.plural(wordA)
            wordBpl = p.plural(wordB)
        except:
            raise Exception("Error: " + wordA + " or " + wordB + " is not a valid word")

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

            try:
                for sent in sents:
                    if re.search(rf"\b{wordA}\b", sent, re.IGNORECASE) or \
                    re.search(rf"\b{wordApl}\b", sent, re.IGNORECASE):
                        sentA.append(sent)
                        sentAn.append(sentence_counter)
                    if re.search(rf"\b{wordB}\b", sent, re.IGNORECASE) or \
                    re.search(rf"\b{wordBpl}\b", sent, re.IGNORECASE):
                        sentB.append(sent)
                        sentBn.append(sentence_counter)
                    sentence_counter += 1
            except: 
                print(f"Words: {wordA} + {wordB}\n Sentence: {sent}")
                raise Exception("Error in textProcessing")

            # if no sentences are found, return
            if len(sentA) == 0 or len(sentB) == 0:
                continue

            # Find the first common sentence between sentA and sentB
            for c in sentAn:
                if c in sentBn:
                    block = sents[c]
                    break

            if 0 < len(block) < N:
                # if block has dollar signs, backslashes and curly brackets, disregard the block
                if re.search(r"[$\\{}]", block):
                    continue


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

                    # if block has dollar signs, backslashes and curly brackets, disregard the block
                    if re.search(r"[$\\{}]", ' '.join(sents[start:end + 1])):
                        continue

                    best_block_length = block_length
                    best_pair = [start, end]

            if best_pair is None:
                continue

            # extract the sentences in text from best_pair[0] to best_pair[1]
            block = ' '.join(sents[best_pair[0]:best_pair[1] + 1])

            if 0 < len(block) < N:
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
        pbar.update()


nlp = English()
nlp.add_pipe("sentencizer")

p = inflect.engine()

# list all files in a folder /users/daychman/Internship_SBERT/files and make the paths absolute
# dir = "/users/daychman/Internship_SBERT/files"
filepath = "/tempo/merged_clean.xml"
# filepath = "/users/daychman/Internship_SBERT/test/parser-test.xml"

length = 46447
# with open(filepath, 'r') as f:
#     length = 0
#     for line in f:
#         length += line.count('</triple>')

# get the folder of filepath
dir = os.path.dirname(os.path.realpath(filepath))
# get the base name of filepath without the extension
base = os.path.basename(filepath).split('.')[0]

os.chdir(dir)
out = open(f"{base}.csv", "w")

out.write("Word A,Word B,Relation,Sentence\n")

handler = XMLHandler(output_file=out)
pbar = tqdm.tqdm(total=length)
parse(filepath, handler)
