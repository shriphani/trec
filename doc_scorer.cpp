#include "doc_scorer.hpp"

using namespace indri::api;

std::string stem_expr(QueryEnvironment *env, std::string& expr) // #1(a b) or #uw8(a b)
{
    int left_p = expr.find('(');
    int right_p = expr.find(')');

    std::string raw_expr = expr.substr(left_p + 1, right_p - left_p - 1);
    std::vector<std::string> terms = split(raw_expr, ' ');

    std::string stemmed_expr = expr.substr(0, left_p); // #1 or #uw8                                                                  
    stemmed_expr += '(';
    for(int i=0;i<terms.size();i++)
        if(terms[i].compare("")!=0)
        {
            stemmed_expr += env->stemTerm(terms[i]);
            if(i!=terms.size()-1)
                stemmed_expr += ' ';
        }
    stemmed_expr += ')';

    return stemmed_expr;
}



double semantic_vector_distance(std::string& term, std::string& snipper) {
    return 0.0;
}

double compute_expression_tf(QueryEnvironment *env, std::string& expression, std::vector<lemur::api::DOCID_T> &docids){
    std::string stemmed_expr = stem_expr(expression);
    
}

// This one is faster than the previous implementation?                                                        
void compute_expression_tfs(std::string &expression, std::vector<lemur::api::DOCID_T> &docids)
{
    std::string stemmed_expr = stem_expr(expression);
    if(expr_tf_done_set.find(stemmed_expr)!=expr_tf_done_set.end())// Has been computed and stored             
        return ;

    std::vector<indri::api::ScoredExtentResult> result = env.expressionList(expression);
    int p = 0; // p is the index for pseudo relevant documents                                                 
    int q = 0; // q is the index for pos list for expression                                                   

    while(p < docids_sorted.size() && q < result.size())
    {
        lemur::api::DOCID_T docid_p = docids_sorted[p];
        lemur::api::DOCID_T docid_q = result[q].document;

        if(docid_p == docid_q)
        {
            // ==== WARNING: Key here is stemmed expression ====                                               
            std::string newkey = stemmed_expr + "+" + tostr(docid_p);
            int occurence = (int)result[q].score; // occurence will be 1 for each in the result                
            expr_doc_tf_map[newkey] += occurence;

            q++;
        }
        else if(docid_p > docid_q)
        {
            q++;
        }
        else // docid_p < docid_q                                                                              
        {
            p++;
        }
    }

    std::cout<<"TFS for RAW:<"<<expression<<"> STEMMED:<"<<stemmed_expr<<"> in "<<docids_sorted.size()<<" docs\
."<<std::endl;

    expr_tf_done_set.insert(stemmed_expr);
}

double score_doc(std::string 

