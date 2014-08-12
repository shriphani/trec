import sys
import math
import xml.etree.ElementTree as ET
import random

def read_test_search(qid, engine):
    searches = []
    engine_id = engine.split('-')[-1]
    
    search_xml_file = '/bos/tmp17/gzheng/FedWeb/fedweb13/FW13-topics-search/%s/%d.xml' % (engine_id, qid)
    tree = ET.parse(search_xml_file)
    samples = tree.getroot()
    
    for search_result in samples:
        for child in search_result:
            if child.tag == 'snippets':
                for ch in child:
                    if ch.tag == 'snippet':
                        searches.append(ch.attrib['id'])

    return searches



def merge(f, qid, top_engines, top_probs):
    N_DOC = 20
    all_searches = dict()
    for engine in top_engines:
        all_searches[engine] = read_test_search(qid, engine)

    sample_probs = []
    sum_prob = 0

    for i in range(0, len(top_probs)):
        sum_prob += top_probs[i]

    for i in range(0, len(top_probs)):
        top_probs[i] = top_probs[i] / sum_prob

    sample_probs.append(top_probs[0])
    
    for i in range(1, len(top_probs)):
        sample_probs.append(sample_probs[-1] + top_probs[i])

    rank = 1
    while rank <= N_DOC:
        prob = random.random()
        
        random_index = -1
        for i in range(0, len(sample_probs)):
            if sample_probs[i] > prob:
                random_index = i
                break

        engine = top_engines[random_index]
        if len(all_searches[engine]) == 0:
            continue

        doc = (all_searches[engine])[0]
        all_searches[engine].pop(0)
        f.write('%d Q0 %s %d -%d CMU\n' % (qid, doc, rank, rank))
        f.flush()
        rank += 1

if __name__ == '__main__':
    if len(sys.argv)!=3:
        print 'Usage: %s <RS_RES> <RM_RES>' % sys.argv[0]
        exit(0)


    TOP_K = 5

    top_engines = []
    top_probs = []

    rm_out = open(sys.argv[2], 'w')
    with open(sys.argv[1], 'r') as rs_in:
        for line in rs_in:
            parts = line.strip().split(' ')
            qid = int(parts[0])
            engine = parts[2]
            rank = int(parts[3])
            score = float(parts[4])
            if rank == 1:
                top_engines = []
                top_probs = []
            
            if rank <= 20:
                top_engines.append(engine)
                top_probs.append(math.exp(score))
                if rank == 20:
                    merge(rm_out, qid, top_engines, top_probs)
            else:
                continue
                
                

            
