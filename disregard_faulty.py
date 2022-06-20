import numpy as np

conv = np.load('/users/daychman/Internship_SBERT/files/conversion.npy')
labels = np.load('/users/daychman/Internship_SBERT/files/labels.npy')
embeddings = np.load('/users/daychman/Internship_SBERT/files/embeddings.npy')

# array([     1,      6, 148984,   2408,  24221,     13,  18298,   5733,
#          16432,   5235,   2531,   5610,  23246, 148234,   2204,      1,
#         148989,    963,      1,   1228,  18474,      1,    157,      6,
#           2490,   2229,   7661,  56705, 267368,   2652, 159895,   9158])

unique, count = np.unique(labels, return_counts=True)

faulty_labels = unique[count < 50]

# get the indices of falty labels
faulty_indices = []
for i in range(len(labels)):
    if labels[i] in faulty_labels:
        faulty_indices.append(i)

# [32384, 32385, 140277, 140278, 351260, 351261, 351263, 351264, 351266, 351267, 351269, 351270, 351272, 351273, 351275, 351276, 579039, 680194, 929676, 929677, 929678, 929679, 929680, 929681, 929682, 929683, 929684, 929685, 929686]

# disregard the faulty indexes in conv and labels and embeddings
conv = np.delete(conv, faulty_labels, axis=0)
labels = np.delete(labels, faulty_indices, axis=0)
embeddings = np.delete(embeddings, faulty_indices, axis=0)

np.save("/users/daychman/Internship_SBERT/files/conversion2.npy", conv)
np.save("/users/daychman/Internship_SBERT/files/labels2.npy", labels)
np.save("/users/daychman/Internship_SBERT/files/embeddings2.npy", embeddings)
