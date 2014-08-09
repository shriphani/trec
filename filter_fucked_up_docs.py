#!/usr/bin/env python
'''
Find unbuilt indices and fix docs.
'''

import magic
import os

INDEX_LOC = '/bos/tmp17/spalakod/trec/fw14/'
DOCS_LOC = '/bos/tmp17/gzheng/FedWeb/fedweb14/FW14-sample-docs/'

def repair_corpus(index_dir):
	'''
	Filter out dirs bro.
	'''
	docs = os.path.join(DOCS_LOC, index_dir)

	for doc in os.listdir(docs):
		if doc.endswith('.html'):
			magic_string = doc, magic.from_file(
				os.path.join(docs, doc)
			)
			if magic_string[-1].find('gzip compressed data') >= 0:
				orig_name = os.path.join(docs, doc)
				orig_name = os.rename(orig_name, orig_name + '.fucked_up')
				print 'renamed:', orig_name


if __name__ == '__main__':
	borked = ['e052', 'e176', 'e068', 'e110', 'e200']

	for engine in borked:
		repair_corpus(engine)