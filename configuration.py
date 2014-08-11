# Put constants and configurations here

WORD_VECTOR_MODELS = [
                       '/bos/usr0/gzheng/TermRecall/src/word2vec/GoogleNews-vectors-negative300.bin',
                       #'/bos/tmp17/gzheng/clueweb09b-new-100.bin',
                       '/bos/tmp17/gzheng/clueweb09b-new-300.bin',
                       #'/bos/tmp17/gzheng/clueweb09b-new-500.bin',
                       #'/bos/tmp17/gzheng/trec7-300.bin'
]


SEARCH_ENGINES_FILE = 'FW13-indices.txt'

RETRIEVAL_MODELS = ['dirichlet', 'okapi']

RETRIEVAL_TOP_DOCS = [1000]

INDRIRUNQUERY = '/bos/usr0/gzheng/.local/bin/IndriRunQuery'

RES_FOLDER = '/bos/tmp17/gzheng/fedweb_res'

SAMPLE_QUERY_FILE = 'FW13-sample-query-terms.txt'

TEST_QUERY_FILE = 'FW13-topics.txt'

RUNID = 'CMU'


