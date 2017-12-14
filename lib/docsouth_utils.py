# -*- coding: iso-8859-15 -*-
#
# utility functions for generating material for DHSM manuscript
#
# James E. Dobson
# Dartmouth College
# James.E.Dobson@Dartmouth.EDU
# http://www.cultcritlab.org

#
# load the entire archive
#

def load_narratives(options="default"):
	import os
	import csv
	import nltk

	docsouth_root = "../na-slave-narratives/data/"
	neh_toc = docsouth_root + "toc.csv"

	# construct a list to store the entire archive
	neh_slave_archive = list()

	row_count=0
	with open(neh_toc, 'rt') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			# deal with the header
			if row_count != 0:
				entry=dict()
				nehid = '{0:03d}'.format(row_count - 1)
				entry['nehid'] = 'neh' + str(nehid)
				file=docsouth_root + "texts/" + row[0].replace(".xml",".txt")
				entry['file'] = file
				entry['author'] = row[1]
				entry['title'] = row[2]

				# try to convert date to an integer (year)
				try:
					year=int(row[3])
				except ValueError:
					year=False
					pass

				entry['year'] = year
				text = open(file,encoding="utf-8").read()

				# option "notokenize" will not read and tokenize texts
				if options != "notokenize":
					tokens = nltk.word_tokenize(text)
					entry['text'] = nltk.Text(tokens)

				# add entry
				neh_slave_archive.append(entry)
			row_count = row_count + 1
	
	# return list, sorted by year
	#neh_slave_archive = sorted(neh_slave_archive, key=lambda k: k['nehid'])
	return(neh_slave_archive)


#
# preprocessing function
#
# This function defines a set of steps to be used in each input text. 
# It does the following: 
#  - removes all non-alpha characters (numbers, stray punctuation, etc)
#  - converts all words to lowercase
#  - removes the above 127 NLTK-defined stopwords
#  - removes an additional set of stopwords
#  - optionally preserves stopwords ("nostop")
#  - optionally preserves only stopwords ("onlystop")
#  - optionally stems words

def preprocess(text_object, options = "default"):
	from nltk.corpus import stopwords
	stopwords = stopwords.words('english')

	# *step one* (default): drop to lowercase 
	pp_text = [word.lower() for word in text_object]

	# *step two* (default): remove non-alpha characters,
	# punctuation, and as many other "noise" elements as
	# possible. If dealing with a single character word, 	
	# drop non-alphabetical characters. This will remove 
	# most punctuation but preserve many words containing
	# marks such as the '-' in 'self-emancipated'

	tmp_text=list()
	for word in pp_text:
		if len(word) == 1 :
			if word.isalpha == True:
				tmp_text.append(word)
		else:
			tmp_text.append(word)		
	pp_text = tmp_text

	# now remove leading and trailing quotation marks, 	
	# hyphens and  dashes
	tmp_text=list()
	for word in pp_text:
		drop_list = ['“','"','”','-','—']
		if word[0] in drop_list:
			word = word[1:]
		if word[-1:] in drop_list:
			word = word[:-1]

		# catch any zero-length words remaining
		if len(word) > 0:
			tmp_text.append(word)

	pp_text = tmp_text

	# preprocessing function: preserve *ONLY* NLTK stopwords
	if options == "onlystop":
		pp_text = [word for word in pp_text if word in stopwords]
		return(pp_text)
       
	# *step three* (default): remove stopwords
	# enable an option for preserving stopwords
	if options != "nostop":
		# add additional stopwords, also containing some remainders from
		# tokenizing
		custom_stopwords="""like go going gone one would got still really get 's 'll"""
		stopwords += custom_stopwords.split()

		pp_text = [word for word in pp_text if word not in stopwords]
        
	return(pp_text)

# Short function to describe object to our best ability
def describe(neh_archive_object):
	if isinstance(neh_archive_object,dict):
		print("NEHID:",neh_archive_object['nehid'])
		print("Author:",neh_archive_object['author'])
		print("Title:",neh_archive_object['title'])
		print("Publication Year:",neh_archive_object['year'])
		stats(neh_archive_object['text'])
	else:	
		print("ERROR: wrong format!")

# some basic statistics 

def stats(text_object):
	import nltk

	if isinstance(text_object,nltk.text.Text):
		token_count = len(text_object)
		raw_vocab = len(text_object.vocab())
	else:
		tokens = nltk.word_tokenize(text_object)
		text_object = nltk.Text(tokens)
		token_count = len(text_object)
		raw_vocab = len(text.vocab())

	pre_processed_text = preprocess(text_object)
	pp_vocab = len(set(pre_processed_text))

	lex_variety=(float(token_count) / float(raw_vocab))
	print("total number of words: " + str(token_count))
	print("total number of unique non-stop words: " + str(raw_vocab))
	print("total number of dropped stopwords:", token_count - len(pre_processed_text))
	print("lexical variety: " + str(round(lex_variety,4)))
