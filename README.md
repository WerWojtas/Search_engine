# Search Engine
Application for searching the most related documents for a given query.
Created by:
- [Weronika Wojtas](https://github.com/WerWojtas)

## System requirements
- Python v 3.8.10
- Flask v 3.0.3
- beautifulsoup4 v 4.12.3
- nltk v 3.8.1
- numpy v 1.17.4
- scipy v 1.10.1

## Initializing and running
To initialize the engine, users need to download documents from specified wiki addresses. The number of pages, starting addresses, and the size of the bag of words can be adjusted in the configuration file.
To initialize engine use command:
```
python initialize.py
```
To run egine use command:
```
python run.py
```

## Query options
Application provides 4 types of different query processing options:
- without SVD : query will be multiplied by term by document matrix
- SVD 10 : term-document matrix will be decomposed into three matrices using Singular Value Decomposition (SVD), retaining 10 singular values
- SVD 100: 100 singular values
- SVD 500: 500 singular values

After submitting a query, 10 documents will be displayed, each with a matching percentage. The document with the highest value will be considered 100% matched.
