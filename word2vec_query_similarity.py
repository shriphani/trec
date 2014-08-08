import gensim
import numpy as np
from collections import defaultdict
from scipy.spatial.distance import cosine

class WordVecSimilarity(object):
    def __init__(self, model_file):
        print 'Loading model %s ...' % model_file
        self.model = gensim.models.Word2Vec.load_word2vec_format(model_file, binary=True)
        print 'Loading model done.'
        self.sim_cache = dict()

    # q is a list of processed terms
    def similarity(self, qid1, q1, qid2, q2):
        if qid1 < qid2:
            cache_key = '%d_%d' % (qid1, qid2)
        else:
            cache_key = '%d_%d' % (qid2, qid1)

        if cache_key in self.sim_cache:
            return self.sim_cache[cache_key]
        
        # meaning not cached yet
            
        terms1 = q1.split(' ')
        terms2 = q2.split(' ')

        # get vec for q1
        q1_vec = None
        rep = None
        for term in terms1:
            try:
                rep = self.model[term.strip()]
            except KeyError:
                print 'KEY ERROR FOR:', term, 'abandoned.'

            if rep != None:
                if q1_vec == None:
                    q1_vec = rep
                else:
                    q1_vec = np.add(q1_vec, rep)


        #get vec for q2
        q2_vec = None
        rep = None
        for term in terms2:
            try:
                rep = self.model[term.strip()]
            except KeyError:
                print 'KEY ERROR FOR:', term, 'abandoned.'

            if rep != None:
                if q2_vec == None:
                    q2_vec = rep
                else:
                    q2_vec = np.add(q2_vec, rep)

        if q1_vec == None or q2_vec == None: # no vector for at least one of the two queries, return default sim, 0?
            sim = 0
        else:
            sim =  1 - cosine(q1_vec, q2_vec)

        self.sim_cache[cache_key] = sim
        return sim
            
            

