#include "tdf_iwf.hpp"

using namespace indri::api;

double scoreTerm(std::string s, QueryEnvironment *env) {
	return env->documentCount(s);
}

double iwf(std::string term, std::map<string, QueryEnvironment *> *m) {
	int score = 0;

	typedef std::map<std::string, QueryEnvironment *>::iterator it_type;
	for(it_type iterator = m->begin(); iterator != m->end(); iterator++) {
    	if ((iterator->second)->documentCount(term) > 0) {
    		score++;
    	}
	}

	return score;
}

double scoreEngineOr(std::string s, QueryEnvironment *env, std::map<string, QueryEnvironment *> *m) {
    std::stringstream ss(s);
    std::string item;

    double score = 0;

    while (std::getline(ss, item, ' ')) {
    	double term_score = scoreTerm(item, env) / iwf(item, m);
        if (item.length() > 0) {
        	if (score < term_score) {
            	score = term_score;
            }
        }
    }
    return score;
}

double scoreEngineAnd(std::string s, QueryEnvironment *env, std::map<string, QueryEnvironment *> *m) {
    std::stringstream ss(s);
    std::string item;

    double score = -1;

    while (std::getline(ss, item, ' ')) {
    	double term_score = scoreTerm(item, env) / iwf(item, m);
        if (item.length() > 0) {
        	if (score < 0) {
            	score = term_score;
            } else if (score > term_score) {
            	score = term_score;
            }
        }
    }
    return score;
}

void addIndices(std::map<string, QueryEnvironment *> *m) {
	std::ifstream file(engines_list.c_str());
	string index;
	while (std::getline(file, index)) {
		try {
			QueryEnvironment *env = new QueryEnvironment();
			env->addIndex(index);
			m->insert(std::pair<string, QueryEnvironment *>(index, env));
		} catch (lemur::api::Exception& e) {
			cout << e.what() << endl;
		}
	}
}

struct sort_pred {
    bool operator()(const std::pair<int,double> &left, const std::pair<int,double> &right) {
        return left.second > right.second;
    }
    };

int main(int argc, char *argv[]) {

  // assume arg1 is query, arg2 is index. - FIXME for entire expt gambit.

  if (argc == 4) { 

  char *query = argv[1];
  char *index = argv[2];
  char *to_select = argv[3];
  
  std::map<string, QueryEnvironment *> engine_index_map;

  addIndices(&engine_index_map);

  if (to_select == "0") {
  	cout << scoreEngineAnd(query, engine_index_map.find(index)->second, &engine_index_map) << endl;
  } else {
  	cout << scoreEngineOr(query, engine_index_map.find(index)->second, &engine_index_map) << endl;
  }
 } else if (argc == 3) {

	char *query = argv[1];

	char *to_select = argv[2];
  
  	std::map<string, QueryEnvironment *> engine_index_map;

  	addIndices(&engine_index_map);

  	std::vector<std::pair<int, double> > vec;
  	std::map<int, string> engine_id;

	typedef std::map<std::string, QueryEnvironment *>::iterator it_type;
	int i = 0;
	for(it_type iterator = engine_index_map.begin(); iterator != engine_index_map.end(); iterator++) {
    	std::pair<int, double> engine_score;
  		if (to_select == "0") {
  			engine_score = make_pair(i, scoreEngineAnd(query, iterator->second, &engine_index_map));
  			vec.push_back(engine_score);
  		} else {
  			engine_score = make_pair(i, scoreEngineOr(query, iterator->second, &engine_index_map));
  			vec.push_back(engine_score);
  		}
  		engine_id.insert(std::pair<int, string>(i, iterator->first));
  		i++;
  	}

    std::sort(vec.begin(), vec.end(), sort_pred());

	for(std::vector<std::pair<int, double> >::iterator it = vec.begin(); it != vec.end(); it++){
		cout << engine_id.find(it->first)->second << " " << it->second << endl;
	}

 } else {
 	cout << "Usage: ./prog_name query index" << endl;
 }
}