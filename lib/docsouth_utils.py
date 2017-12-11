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
				entry['index'] = row_count
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
				text = open(file).read()

				# option "notokenize" will not read and tokenize texts
				if options != "notokenize":
					tokens = nltk.word_tokenize(text)
					entry['text'] = nltk.Text(tokens)

				# add entry
				neh_slave_archive.append(entry)
			row_count = row_count + 1
	
	# return list, sorted by year
	neh_slave_archive = sorted(neh_slave_archive, key=lambda k: k['index'])
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

def preprocess(text,options="default"):


	# default: drop to lowercase and remove non alpha characters
	pp_text = [word for word in text if word.isalpha() ]
	pp_text = [word.lower() for word in pp_text]

	# preprocessing function: preserve *ONLY* stopwords
	if options == "onlystop":
		from nltk.corpus import stopwords
		stopwords = stopwords.words('english')
		pp_text = [word for word in pp_text if word in stopwords]
		return(pp_text)
        
	# enable an option for preserving stopwords
	if options != "nostop":
		from nltk.corpus import stopwords
		stopwords = stopwords.words('english')
		custom_stopwords="""like go going gone one would got still really get"""
		stopwords += custom_stopwords.split()
		pp_text = [word for word in pp_text if word not in stopwords]
        
	return(pp_text)



def stats(text):
        import nltk
        tokens = nltk.word_tokenize(text)
        text = nltk.Text(tokens)
        lines = raw_text.count('\n')
        pre_processed_text = preprocess(text)
        vocab = len(set(pre_processed_text))
        lex_variety=(float(len(tokens)) / float(vocab))
        print("object:",input_file)
        print("total number of lines: " + str(lines))
        print("total number of words: " + str(len(tokens)))
        print("total number of unique non-stop words: " + str(vocab))
        print("total number of dropped stopwords: " + str(len(tokens) - len(pre_processed_text)))
        print("lexical variety: " + str(round(lex_variety,4)))
