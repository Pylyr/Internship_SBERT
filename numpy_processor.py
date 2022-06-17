import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
import os

file = '/users/daychman/Internship_SBERT/files/merged'

#convert df into a numpy array
df = pd.read_csv(file)

# drop the columns word A and word B
df = df.drop(['Word B', 'Word A'], axis=1)

# convert the relationships into categories
rel_cat = df['Relation'].astype('category')

# label each unique value in the column 'Relation' with a number
labels = rel_cat.cat.codes.to_numpy()

# get the conversion dictionary between the labels and the numbers
conversion_dict = np.array(list(enumerate(rel_cat.cat.categories)))

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

#Sentences are encoded by calling model.encode()
arr = model.encode(df['Sentence'])

dir = os.path.dirname(os.path.realpath(file))
os.chdir(dir)

np.save("embeddings.npy", arr)
np.save("labels.npy", labels)
np.save("conversion.npy", conversion_dict)
