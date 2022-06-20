from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.metrics import cluster
import numpy as np

new_dimension = 50
n_relations = 25

print('Importing embeddings...')

conv = np.load('/users/daychman/Internship_SBERT/files/conversion2.npy')
labels = np.load('/users/daychman/Internship_SBERT/files/labels2.npy')
embeddings = np.load('/users/daychman/Internship_SBERT/files/embeddings2.npy')

print('Calculating PCA...')

#Compute PCA on the train embeddings matrix
pca = PCA(n_components=new_dimension)
pca.fit(embeddings)
transformed = pca.transform(embeddings)

print('Clustering...')

kmeans = KMeans(n_clusters=n_relations).fit(transformed)

print('Calculating the score...')

def purity_score(y_true, y_pred):
    contingency_matrix = cluster.contingency_matrix(y_true, y_pred)
    return np.sum(np.amax(contingency_matrix, axis=0)) / np.sum(contingency_matrix)

print(purity_score(labels, kmeans.labels_))