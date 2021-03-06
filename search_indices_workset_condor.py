from main import read_queries, read_engines
from configuration import *

import os
import os.path

if __name__ == '__main__':
    engines = read_engines(SEARCH_ENGINES_FILE)
    test_queries = read_queries(TEST_QUERY_FILE)
    
    for qid in TEST_QUERIES_OFFICIAL: #test_queries:
        qstr = test_queries[qid]
        
        for engine in engines:
            engine_parts = engine.split('/')
            for rm in RETRIEVAL_MODELS:
                terms = qstr.split(' ')
                for term in terms:
                    term = term.strip()
                    
                    jobstr = '%s/%s_%d_%s_%s' % (RES_FOLDER, engine.split('/', 4)[-1].replace('/', '_'), qid, rm, term)
                    jobname = '%s.job' % jobstr
                    res_filename = '%s.res' % jobstr
                    
                    if os.path.isfile(res_filename):
                        continue

                    query_file = '%s.q' % jobstr
                    
                    qf = open(query_file, 'w')
                    qf.write('<parameters>\n<query><type>indri</type><number>%d</number><text>\n%s\n</text>\n' % (qid, term))
                    
                    initial_res_file = '%s/%s_%d_%s.res' % (RES_FOLDER, engine.split('/', 4)[-1].replace('/', '_'), qid, rm)
                    with open(initial_res_file, 'r') as initial_res_f:
                        for line in initial_res_f:
                            parts = line.strip().split(' ')
                            docno = parts[2].strip()
                            qf.write('<workingSetDocno>%s</workingSetDocno>\n' % docno)

                    qf.write('</query>\n</parameters>')
                    qf.close()
                        
                    print res_filename
                    f = open(jobname, 'w')
                    f.write('Universe = vanilla\n')
                    f.write('initialdir = /bos/usr0/gzheng/IRLab/trec\n')
                    f.write('executable = /bos/usr0/gzheng/.local/bin/IndriRunQuery\n')
                    search_param = ' %s -index=%s -count=1000 -trecFormat=t -rule=method:%s' % (query_file, engine, rm)
                    f.write('arguments = %s\n' %( search_param))
                    f.write('output = %s\n' % res_filename)
                    f.write('log = '+jobstr+'.log\n')
                    f.write('error = '+jobstr+'.err\n')
                    f.write('queue\n')
                    f.close()
                    os.system('condor_submit '+ jobname)

    
