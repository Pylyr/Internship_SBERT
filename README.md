downloader.sh - bash script to download the files
google_drive_download - similar script to download files from google drive
serial/parallel_processor.py - used to extract the best block containing both words from the abstract
xml_merger.ipynb - merges processed xmls into one big xml removing the headers
numpy_processor.ipynb/py - encodes the category as a number and the sentence using paraphrase-MiniLM-L6-v2
word_embeddeer.ipynb/py - batch uncased SBERT embedding + 2 concatenated contextual BERT embeddings of the keywords
acronyms_decoder.ipynb - used to reverse engineer back the acronyms using in the text for better embeddings
fine_tunning:
1 - neural network with the softmax layer removed
2 - huggingface hinge loss
3 - huggingface triplet loss
pca.ipynb - final file for testing, plotting and evaluating the results
