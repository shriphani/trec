/* 
header file for TDF-IWF 
Like TF-IDF but we compute:

TDF : #of documents containing a term
---
IWF : # of resources containing this term

*/

#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include "indri/QueryEnvironment.hpp"
#include "lemur/Exception.hpp"

std::string engines_list = "indices.txt"; // list of engines
