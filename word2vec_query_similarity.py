import gensim
from collections import defaultdict

class WordVecSimilarity(object):
    def __init__(self, model_file):
        print 'Loading model %s ...' % model_file
        #self.model = gensim.models.Word2Vec.load_word2vec_format(model_file, binary=True)
        print 'Loading model done.'

    # q is a list of processed terms
    def similarity(self, q1, q2):
        return 1.0

        try:
            rep = model[term]
        except KeyError:
            print 'KEY ERROR FOR:', ' ', 'abandoned.'
            

