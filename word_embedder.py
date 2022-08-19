import numpy as np
import gensim.downloader as api
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch
import re
from tqdm import tqdm
import time

file = 'merged_clean.csv'
definitions = np.load("definitions.npy", allow_pickle=True).item()
embeddings = np.load('embeddings.npy')

df = pd.read_csv(file)
words_corr = df[['Word A', 'Word B']].to_numpy()
sentences = df['Sentence'].to_numpy()

layers = [-4, -3, -2, -1]
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# model = AutoModel.from_pretrained("bert-base-uncased", output_hidden_states=True)

model = AutoModel.from_pretrained("bert-base-uncased", output_hidden_states=True)
model.to(device)

def levenshtein(word1, word2):
    """Calculate the Levenshtein distance between two words."""
    if len(word1) > len(word2):
        word1, word2 = word2, word1
    distances = range(len(word1) + 1)
    for index2, letter2 in enumerate(word2):
        distances_ = [index2 + 1]
        for index1, letter1 in enumerate(word1):
            if letter1 == letter2:
                distances_.append(distances[index1])
            else:
                distances_.append(1 + min((distances[index1], distances[index1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]    

# def levenshtein(word1, word2):
#     return np.sum(np.array(list(map(lambda x: x[0] != x[1], zip(word1, word2)))))

def get_word_idx(sent: str, word: str):
    # word can be 1-3 words long. Find the closest match in the sentence using regex.
    words = re.findall(r'\w+', sent)
    # find the closest match in the sentence using Levenshtein distance 
    word_idx = min(range(len(words)), key=lambda i: levenshtein(word, words[i]))
    return word_idx


def batch_word_vector_BERT(sent_list, word_list):
    splitted_words_list = [definitions.get(word, word).split() for word in word_list]
    token_ids_list = [[get_word_idx(sent, word) for word in words] for sent, words in zip(sent_list, splitted_words_list)]
    
    if isinstance(sent_list, np.ndarray):
        sent_list = sent_list.tolist()

    encoded_list = tokenizer(sent_list, return_tensors="pt", padding=True, truncation=True)

    token_ids = []
    for i in range(len(token_ids_list)):
        idx = encoded_list.word_ids(i)
        token_ids.append([])
        for j in range(len(idx)):
            if idx[j] in token_ids_list[i]:
                token_ids[i].append(j)

    encoded_list.to(device)
    with torch.no_grad():
        output = model(**encoded_list)

    # Get all hidden states
    states = output.hidden_states
    # Stack and sum all requested layers
    output = torch.stack([states[i] for i in layers]).sum(0)
    # Only select the tokens that constitute the requested word
    word_tokens_output = [output[i][token_ids[i]] for i in range(len(output))]
    word_vectors = [tensor.mean(0) for tensor in word_tokens_output]
    v_list = [tensor.numpy() for tensor in word_vectors]
    # convert a list of tensors to a numpy array
    return np.array(v_list)


    # return np.mean(word_vectors, axis=0)

def process_embeddings(start=0, end=len(embeddings)):
    global embeddings, words_corr, sentences
    # cut the embeddings to the desired range
    embeddings = embeddings[start:end]
    sentences = sentences[start:end]
    words_corr = words_corr[start:end]


    concat_embeddigs = []

    batch_size = 100
    n = np.ceil(len(embeddings)/batch_size).astype(int)
    for i in tqdm(range(n)):
        words_corr_batch = words_corr[i*batch_size:(i+1)*batch_size]
        words1, words2 = words_corr_batch[:, 0], words_corr_batch[:, 1]
        sent_batch = sentences[i*batch_size:(i+1)*batch_size]
        embeddings_batch = embeddings[i*batch_size:(i+1)*batch_size]
        try :
            vec1 = batch_word_vector_BERT(sent_batch, words1)
            vec2 = batch_word_vector_BERT(sent_batch, words2)
            concat_embeddigs.append(np.concatenate((vec1, vec2, embeddings_batch), axis=1))
        except:
            raise ValueError("Error in sentence: " + str(i))
    concat_embeddigs = np.array(concat_embeddigs).reshape(-1, 1920)
    np.save(f'concat_embeddings ({start}-{end})', concat_embeddigs)

process_embeddings(start=700_000)
