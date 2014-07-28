# TREC Federated Search Clueweb

## Dataset:

location: /bos/tmp17/gzheng/FedWeb

observations: In FW14, 10 results per query and all snippets have associated html documents (what to do if results are jpeg or such?)

Guoqing: Aren't JPEGs just thumbs for the pages? - looks like that is the case.

Indices for each collection: [indices.txt](indices.txt)
IndriBuildIndex segfaulted on 4 collections (possibly a memory error).

Implementation of that naive TFIDF based model from last year in [tdf_iwf.cpp](tdf_iwf.cpp).

Guoqing: I think we were trying to do the TWF.IRF model first? TWF of a node at an upper level is just the sum of the TWF.IDFs of its children. If the TDF.IWF is not what I understand TWF.IRF above, I can do the TWF.IRF part.


To run:
```
make
./tdf_iwf "barack obama" 0  (searches using AND operator, use 1 for searching with OR).
```

## Plan:

* Build indri indices for all collections - almost done.
* Implement winning idea for 2013. - done
* REDDE/CORI etc because whatever.

## Misc:

Indri API: http://www.lemurproject.org/doxygen/lemur/html/classindri_1_1api_1_1QueryEnvironment.html#a26
