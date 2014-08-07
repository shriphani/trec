import sys
import configuration
import word2vec_query_similarityo

# main entry for all three tasks here

def read_queries(query_file):
    queries = []
    with open(query_file, 'r') as qf:
        for line in qf:
            parts = lint.strip().split(':')
            qid = int(parts[0])
            query = parts[1].strip()

        queries.append((qid, query))

    return queries

def read_engines(engine_file):
    engines = []
    with open(engine_file, 'r') as ef:
        for line in ef:
            engines.append(line.strip())

    return engines

if __name__ == '__main__':
    
    wv_model = WordVecSimilarity(WORD_VECTOR_MODELS[-1])
    
    test_queries = read_queries(TEST_QUERY_FILE)
    sample_queries = read_queries(SAMPLE_QUERY_FILE)

    engines = read_engines(SEARCH_ENGINES_FILE)
    
    
    
    
