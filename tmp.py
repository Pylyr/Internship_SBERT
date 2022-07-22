import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#Sentences are encoded by calling model.encode()
arr = model.encode("mama")

print(arr)
print(arr.shape)