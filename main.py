from configuration import *
from word2vec_query_similarity import *

import sys
import gc
import os
import math
import string
import os.path

# main entry for all three tasks here

def query_preprocess(query_str):
    exclude = set(string.punctuation)
    qstr_processed = ''.join(ch for ch in query_str if ch not in exclude)
    return qstr_processed

def read_queries(query_file):
    queries = dict()
    with open(query_file, 'r') as qf:
        for line in qf:
            parts = line.strip().split(':')
            qid = int(parts[0])
            query = query_preprocess(parts[1].strip())
            queries[qid] = query

    return queries

def read_engines(engine_file):
    engines = []
    with open(engine_file, 'r') as ef:
        for line in ef:
            engines.append(line.strip())

    return engines

def indri_score(raw_score, rm):
    return math.exp(raw_score)
    
    ''' # this needs to be confirmed 
    if rm == 'dirichlet':
        return math.exp(raw_score)
    elif rm == 'okapi':
        return raw_score
    '''

def read_resource_vertical_mapping(resource_vertical_mapping_file):
    rv_dict = dict()
    with open(resource_vertial_mapping_file, 'r') as rv_mapping:
        for line in rv_mapping:
            if not line.startswith('FW14'):
                continue
            
            parts = line.split('\t')
            engine_id = parts[0].strip()
            vertical_id = parts[-1].strip()
            rv_dict[engine_id] = vertical_id


    return rv_dict

def resource_selection(wv_model, sample_queries, test_queries, engines, rm, res_result_file):
    with open(res_result_file, 'w') as res_out:#, open(vertical_result_file, 'w') as ver_out:
        for qid in TEST_QUERIES_OFFICIAL: #test_queries:
            resource_score_list = []
            qstr = test_queries[qid]

            for engine in engines:
                engine_parts = engine.split('/')
                engine_id = '%s-%s' % (engine_parts[-2].upper(), engine_parts[-1])
                res_filename = '%s/%s_%d_%s.res' % (RES_FOLDER, engine.split('/',4)[-1].replace('/', '_'), qid, rm)
                if os.path.isfile(res_filename):
                    print 'READ CACHE SEARCH FOR QID: %d QUERY: %s WITH ENGINE: %s ... ' % (qid, qstr, engine)
                else:
                    search_cmd = '%s -query.number=%d -query.text=\"%s\" -index=%s -count=1000 -trecFormat=t -rule=method:%s > %s' % ( INDRIRUNQUERY, qid, qstr, engine, rm, res_filename)
                    print 'SEARCHING QID: %d QUERy: %s WITH ENGINE: %s ... ' % (qid, qstr, engine)
                    os.system(search_cmd)

                with open(res_filename, 'r') as engine_res_file:
                    resource_score = 0
                    for line in engine_res_file:
                        parts = line.strip().split(' ')
                        docno = parts[2].strip()
                        rank = int(parts[3])
                        indri_raw_score = float(parts[4])
                        score = indri_score(indri_raw_score, rm)

                        sample_qid = int(docno.split('/')[-1].split('_')[0])
                        sample_qstr = sample_queries[sample_qid]

                        wv_similarity = wv_model.similarity(sample_qid, sample_qstr, qid, qstr)
                        print '== WORD VECTOR SIMILARITY OF # %s AND %s # IS %f ==' % (sample_qstr, qstr, wv_similarity)

                        #resource_score += math.exp(wv_similarity) * score
                        resource_score += wv_similarity * score

                resource_score_list.append((resource_score, engine_id))

            resource_score_list.sort(reverse=True)

            resource_rank = 1
            vertical_score_dict = dict()
            for record in resource_score_list:
                res_out.write('%d Q0 %s %d %f %s\n' % (qid, record[1], resource_rank, record[0], RUNID))
                resource_rank += 1
'''
                vertical = rv_dict[record[1]]
                if vertical in vertical_score_dict:
                    vertical_score_dict[vertical] += record[0]
                else:
                    vertical_score_dict[vertical] = record[0]

            vertical_score_list = []
            for key, value in vertical_score_dict.iteritems():
                vertical_score_list.append((value, key))

            vertical_score_list.sort(reverse=True)
            
            # NOTE HERE ONLY OUTPUT TOP 10 VERTICALS
            top_verticals = 10
            for record in vertical_score_list[:top_verticals]:
                ver_out.write('%d %s %s\n' % (qid, record[1], RUNID))
'''

def resource_selection_tw(wv_model, sample_queries, test_queries, engines, rm, res_result_file):
    with open(res_result_file, 'w') as res_out:#, open(vertical_result_file, 'w') as ver_out:
        for qid in TEST_QUERIES_OFFICIAL: #test_queries:
            resource_score_list = []
            qstr = test_queries[qid]
            
            for engine in engines:
                resource_score = 0
                
                engine_parts = engine.split('/')
                engine_id = '%s-%s' % (engine_parts[-2].upper(), engine_parts[-1])
                res_filename = '%s/%s_%d_%s.res' % (RES_FOLDER, engine.split('/',4)[-1].replace('/', '_'), qid, rm)
                if os.path.isfile(res_filename):
                    print 'READ CACHE SEARCH FOR QID: %d QUERY: %s WITH ENGINE: %s ... ' % (qid, qstr, engine)
                else:
                    search_cmd = '%s -query.number=%d -query.text=\"%s\" -index=%s -count=1000 -trecFormat=t -rule=method:%s > %s' % ( INDRIRUNQUERY, qid, qstr, engine, rm, res_filename)
                    print 'SEARCHING QID: %d QUERy: %s WITH ENGINE: %s ... ' % (qid, qstr, engine)
                    os.system(search_cmd)


                terms = qstr.split(' ')
                for term in terms:
                    term = term.strip()

                    tw_res_filename = '%s/%s_%d_%s_%s.res' % (RES_FOLDER, engine.split('/',4)[-1].replace('/', '_'), qid, rm, term)
                    
                    if os.path.isfile(tw_res_filename):
                        print 'READ CACHE SEARCH FOR QID: %d TERM: %s WITH ENGINE: %s ... ' % ( qid, term, engine)
                    else:
                        print ' ********* ERROR: NO CACHE FOR FOR QID: %d TERM: %s WITH ENGINE: %s ... ' % ( qid, term, engine)
                        continue

                    with open(tw_res_filename, 'r') as tw_res_file:
                        for line in tw_res_file:
                            parts = line.strip().split(' ')
                            docno = parts[2]. strip()
                            indri_raw_score = float(parts[4])
                            score = indri_score(indri_raw_score, rm)
                            
                            sample_qid = int(docno.split('/')[-1].split('_')[0])
                            sample_qstr = sample_queries[sample_qid]
                            
                            wv_query_term_sim = wv_model.similarity_query_term(sample_qstr, term)
#                            resource_score += math.exp(wv_query_term_sim) * score
                            resource_score += wv_query_term_sim * score

                resource_score_list.append((resource_score, engine_id))
            
            resource_score_list.sort(reverse=True)
            
            resource_rank = 1
#            vertical_score_dict = dict()
            for record in resource_score_list:
                res_out.write('%d Q0 %s %d %f %s\n' % (qid, record[1], resource_rank, record[0], RUNID))
                resource_rank += 1
'''
                vertical = rv_dict[record[1]]
                if vertical in vertical_score_dict:
                    vertical_score_dict[vertical] += record[0]
                else:
                    vertical_score_dict[vertical] = record[0]

            vertical_score_list = []
            for key, value in vertical_score_dict.iteritems():
                vertical_score_list.append((value, key))

            vertical_score_list.sort(reverse=True)
            
            # NOTE HERE ONLY OUTPUT TOP 10 VERTICALS
            top_verticals = 10
            for record in vertical_score_list[:top_verticals]:
                ver_out.write('%d %s %s\n' % (qid, record[1], RUNID))
'''


# for 2013, pages for testing queries are provided
#def result_merging_2013():

# for 2014, no page for testing queries are provided
#def result_merging_2014():

def get_wordvector_id(modelfile):
    if 'GoogleNews' in modelfile:
        return 'G'
    else:
        return 'C'

if __name__ == '__main__':
    test_queries = read_queries(TEST_QUERY_FILE)
    sample_queries = read_queries(SAMPLE_QUERY_FILE)
    engines = read_engines(SEARCH_ENGINES_FILE)

    for wv_model_file in WORD_VECTOR_MODELS:
        wv_model = WordVecSimilarity(wv_model_file)
        #    wv_model = WordVecSimilarity(WORD_VECTOR_MODELS[0])

        for rm in RETRIEVAL_MODELS:
            res_result_file = 'cmu-RS-%s-%s-QQ.res' % (rm, get_wordvector_id(wv_model_file))
            rw_res_result_file = 'cmu-RS-%s-%s-TQ.res' % (rm, get_wordvector_id(wv_model_file))
            resource_selection(wv_model, sample_queries, test_queries, engines, rm, res_result_file)
            resource_selection_tw(wv_model, sample_queries, test_queries, engines, rm, rw_res_result_file)

        gc.collect()
