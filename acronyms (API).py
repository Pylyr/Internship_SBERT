import requests
import bs4
import time 

acronyms = ['aco', 'ade', 'alp', 'ann', 'anns', 'asp', 'asr', 'bcis', 'cart', 'ccg', 'cnn', 'cnns', 'cob', 'code', 'crt', 'cvc3', 'dibr', 'dpps', 'eeg', 'eer', 'elm', 'emf', 'fcms', 'gaze', 'gene', 'git', 'glcm', 'gps', 'gpus', 'gra', 'hci', 'hmm', 'hog', 'ica', 'ilp', 'join', 'key', 'knn', 'lda', 'lens', 'lfda', 'lift', 'lmis', 'lts', 'lvq', 'md5', 'mlp', 'msi', 'ner', 'nlp', 'nmf', 'obda', 'ocl', 'opc', 'path', 'pca', 'pin', 'pnn', 'pso', 'rbac', 'rbf', 'rdf', 'rnns', 'rtec', 'sat', 'spin', 'star', 'surf', 'svm', 'svms', 'tag', 'uml', 'vpa', 'word', 'xml']

def acronym_finder(acronym):
    """
    This function takes a string and returns the definition of the acronym.
    """
    global count

    url = f"https://www.acronymfinder.com/Information-Technology/{acronym}.html"
    response = requests.get(url)
    # find the class "result-list__body__meaning"
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    meaning = soup.find(class_="result-list__body__meaning")
    if meaning is None:
        return "No definition found"
    count += 1
    return meaning.text

count = 0


for acronym in acronyms:
    print(f"{acronym} -> {acronym_finder(acronym)}")
    print()
    time.sleep(10)

print(count / len(acronyms))