# Tabular data semantics for Python


## Source dependencies
- [Python 3](https://www.python.org/)
- [Owlready2](https://pypi.org/project/Owlready2/): pip3 install Owlready2
- [SPARQLWrapper](https://pypi.org/project/SPARQLWrapper/): pip3 install SPARQLWrapper
- [urllib](https://docs.python.org/3/library/urllib.html): pip3 install urllib.request, pip3 install urllib.parse (probably not required)

## More dependecies:
- gensim: conda install -c conda-forge gensim
- textblob
- nltk

# File dependencies
- wiki-news-300d-1M.vec from fastText

An interface to ask queries to the KGs (DBpedia and Wikidata) via lookup (query strings to retrieve candidate entities) and relationships  in the KG (via the sparql endpoint) (author @ernestojimenezruiz)
+ an answer type classification system that uses word and KG embeddings to retrieve semantic meaning (author @eljne)