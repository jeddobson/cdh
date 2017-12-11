# import required tools
import csv
import nltk
import os, sys

# import textmine library
import docsouth_utils

neh_slave_archive = docsouth_utils.load_narratives()

import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

#
# create input list of documents for the vectorizer
# and perform additional preprocessing (stopword removal, 
#  lowercase, dropping non-alpha characters, etc.)
#

neh_slave_archive_texts=list()
for i in neh_slave_archive:
    preprocessed=docsouth_utils.preprocess(i['text'])
    neh_slave_archive_texts.append(' '.join(preprocessed))


from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(strip_accents='unicode',stop_words='english',lowercase=True)

trans_matrix = vectorizer.fit_transform(neh_slave_archive_texts)
trans_matrix = trans_matrix.toarray()


# calculate euclidean distance between each text
from sklearn.metrics.pairwise import euclidean_distances
euclidean_dist_matrix = euclidean_distances(trans_matrix)


# calculate cosine similarity distances between each text
from sklearn.metrics.pairwise import cosine_similarity
cosine_dist_matrix = 1 - cosine_similarity(trans_matrix)


print(np.round(min(cosine_dist_matrix[12,1],2)))
#print(max(euclidean_dist_matrix[12,1]))
print(np.argmin(cosine_dist_matrix))
print(np.argmin(euclidean_dist_matrix))


neh_slave_archive[199]['title']

# distance between douglass and the other texts 
douglass_1845_narrative=199
dougdiff_dict={}
i=0
for text in neh_slave_archive: 
    dougdiff_dict[i] = np.round(cosine_dist_matrix[199,i],3)
    i=i+1

# display sorted distances from douglass
for x in sorted(dougdiff_dict, key=dougdiff_dict.__getitem__):
    print(neh_slave_archive[x]['file'],dougdiff_dict[x])


