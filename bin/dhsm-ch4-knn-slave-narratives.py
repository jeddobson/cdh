#!/usr/bin/env python


# load required packages
import sys, os
import re
import operator
import nltk

from nltk import pos_tag, ne_chunk
from nltk.tokenize import wordpunct_tokenize

# load local library
sys.path.append("../lib")
import docsouth_utils

# each dictionary entry in the 'list' object returned by load_narratives 
# contains the following keys:
#  'author' = Author of the text (first name, last name)
#  'title' = Title of the text
#  'year' = Year published as integer or False if not simple four-digit year
#  'file' = Filename of text
#  'text' = NLTK Text object

neh_slave_archive = docsouth_utils.load_narratives()

#
# establish two simple classes for kNN classification
# the "date" field has already been converted to an integer
# all texts published before 1865, we'll call "antebellum"
# "postbellum" for those after.
#

period_classes=list()

for entry in neh_slave_archive:
    file = entry['file']
    if entry['year'] != False and entry['year'] < 1865:
        period_classes.append([file,"antebellum"])
    if entry['year'] != False and entry['year'] > 1865:  
        period_classes.append([file,"postbellum"])

# create labels as a list        
labels=[i[1] for i in period_classes]

# create list of filenames 
files=[i[0] for i in period_classes]

#
# create training and test datasets
# leave out fifty files, the last fifty with integer dates from the toc, for testing
#

test_size=75

train_labels=labels[:-test_size]
train_files=files[:-test_size]

# the last set of texts (test_size) are the "test" dataset (for validation)
test_labels=labels[-test_size:]
test_files=files[-test_size:]

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

# intialize the vectorizer
vectorizer = HashingVectorizer(stop_words='english',
                               input='filename',
                               non_negative=True)

training_data = vectorizer.transform(train_files)
test_data=vectorizer.transform(test_files)

# display sizes
print("training data:")
for period in ['postbellum', 'antebellum']:
    print(" ",period,":",train_labels.count(period))
    
print("test data:")
for period in ['postbellum', 'antebellum']:
    print(" ",period,":",test_labels.count(period))

# run kNN and fit training data
knn = KNeighborsClassifier(n_neighbors=13)
knn.fit(training_data,train_labels)

# Predict results from the test data and check accuracy
pred = knn.predict(test_data)
score = metrics.accuracy_score(test_labels, pred)
print("accuracy:   %0.3f" % score)
print(metrics.classification_report(test_labels, pred))
print("confusion matrix:")
print(metrics.confusion_matrix(test_labels, pred))

